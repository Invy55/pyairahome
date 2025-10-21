"""BLE interaction class for Aira Home."""
# ble.py
from cryptography.hazmat.primitives.asymmetric import padding
from .device.heat_pump.ble.v1.get_data_pb2 import GetData, DataResponse
from .device.heat_pump.ble.v1.chunked_message_pb2 import ChunkedMessage
from .utils import Utils, BLEDiscoveryError, BLEConnectionError
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.primitives import hashes
from .util.v1.uuid_pb2 import Uuid as Uuid1
from google.protobuf.message import Message
from bleak import BleakScanner, BleakClient
from bleak.backends.device import BLEDevice
from .enums import GetDataType
import concurrent.futures
from uuid import UUID
from enum import Enum
import asyncio
import os


class Ble:
    """A client to interact with Aira devices over Bluetooth Low Energy (BLE)."""

    def __init__(self, airahome_instance, ext_loop: asyncio.AbstractEventLoop | None = None):
        """Initialize Cloud with reference to parent AiraHome instance."""
        self._ah_i = airahome_instance
        self.logger = self._ah_i.logger

        self.logger.debug("Initializing BLE instance")

        # setup asyncio loop, if explicitly provided use that one, otherwise try to get the running loop or create a new one
        self.loop = None
        if ext_loop is not None:
            # explicitly provided external loop — always prefer this
            self.loop = ext_loop
        else:
            try:
                # try to get currently running loop (should work in any async context)
                self.loop = asyncio.get_running_loop()
            except RuntimeError:
                # no loop is running (called from sync context) — create a new event loop
                self.loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.loop)
        self.lock = asyncio.Lock()

        # store discovered devices to avoid rescanning
        self._discovery_cache = {} # uuid -> BleDevice
        # create an empty scanner variable
        self._scanner = None

        # store parts of received messages to reassemble them afterwards
        self._parts = {}
        self._lengths = {}

        self._client = None

    ###
    # Helper methods
    ###

    def _get_scanner(self) -> BleakScanner:
        """Get or create the BleakScanner instance."""
        if not self._scanner:
            self._scanner = BleakScanner(detection_callback=self._on_device_adv)
        return self._scanner

    def _run_async(self, coro, *args, **kwargs):
        """Helper method to run async methods."""
        if self.loop.is_running():
            # Loop is already running (HA or generic async context)
            future = asyncio.run_coroutine_threadsafe(coro(*args, **kwargs), self.loop)
            return future.result()
        else:
            # Created loop (sync context)
            return self.loop.run_until_complete(coro(*args, **kwargs))

    def _on_device_adv(self, device, adv_data):
        """Callback for handling device advertisement events."""
        # Check for manufacturer data with company ID 0xFFFF (read below about this)
        if adv_data.manufacturer_data:
            for company_id, data_bytes in adv_data.manufacturer_data.items():
                if company_id == 0xFFFF:
                    try:
                        uuid = str(UUID(data_bytes.hex()))
                        self.logger.debug(f"Discovered potential Aira device: {uuid} - {device.name} ({device.address})")
                    except Exception as e:
                        self.logger.debug(f"Failed to parse UUID from manufacturer data: {e}")
                        uuid = None
                    if uuid:
                        self._discovery_cache[uuid] = device
                        return

    def _on_disconnect(self, client: BleakClient):
        """Callback for handling disconnection events."""
        self.logger.info("BLE device disconnected")
        self._client = None

    def _on_notify(self, sender: int, data: bytearray):
        """Callback for handling notifications from the BLE device."""
        try:
            chunk = ChunkedMessage()
            chunk.ParseFromString(data)

            message_id = chunk.message_id.value.hex() # messages ids are stored as normal hex data
            if message_id not in self._parts:
                self._parts[message_id] = {}
                self._lengths[message_id] = chunk.total_bytes
            self._parts[message_id][chunk.byte_offset] = chunk.content
            self.logger.debug(f"Received BLE chunk: message_id={message_id}, byte_offset={chunk.byte_offset}, total_bytes={chunk.total_bytes}, content_length={len(chunk.content)}")
        except:
            pass # NOT A CHUNKED MESSAGE

    def _rsa_encrypt(self, input_bytes: bytes) -> bytes:
        if not self._ah_i._cert:
            raise ValueError("No certificate loaded for encryption.")
        
        public_key = self._ah_i._cert.public_key()

        # Encrypt the input bytes using RSA with PKCS1 OAEP padding
        ciphertext = public_key.encrypt(
            input_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return ciphertext

    def _send_ble(self, characteristic: str, message: Message, encrypt: bool = False):
        """Send a protobuf message to the connected BLE device. Splits the message into chunks if it exceeds the MTU size. If `encrypt` is True, the message will be encrypted with the certificate key."""
        if not self.is_connected():
            raise BLEConnectionError("Not connected to any BLE device.")
        
        data = message.SerializeToString()
        payload_size = self._ah_i.max_ble_chunk_size

        # chunk the message if it exceeds the payload size or if it must be encrypted, since encrypting will increase the size to 256 bytes
        chunks = [None]
        if len(data) > payload_size or encrypt:
            chunks = [data[i:i + payload_size] for i in range(0, len(data), payload_size)]
            message_id = getattr(data, 'message_id', os.urandom(16)) # if the message has a message_id use it, otherwise generate a random one
            for i,chunk in enumerate(chunks):
                content = chunk if not encrypt else self._rsa_encrypt(chunk)
                chunked_message = ChunkedMessage(
                    message_id=Uuid1(value=message_id),
                    byte_offset=i * payload_size,
                    total_bytes=len(content),
                    content=content
                )
                chunk_data = chunked_message.SerializeToString()
                self._run_async(self._client.write_gatt_char, char_specifier=characteristic, data=chunk_data)
        
        self._run_async(self._client.write_gatt_char, char_specifier=characteristic, data=data)
        self.logger.debug(f"Sent BLE message on characteristic {characteristic} (length: {len(data)} bytes, chunks: {len(chunks)})")

    def _wait_for_response(self, message_id: Uuid1, timeout: int = -1) -> bytes:
        if timeout < 0:
            timeout = self._ah_i.ble_notify_timeout

        reconstructed = None
        msg_id_hex = message_id.value.hex()
        for i in range(timeout * 10):
            self._run_async(asyncio.sleep, 0.1) # sleep

            # check if the sum of part lenghts equals the actual total
            if not self._lengths.get(msg_id_hex, False):
                continue

            parts_dict = self._parts.get(msg_id_hex, {})
            total_received = sum([len(part) for part in parts_dict.values()])
            expected_total = self._lengths[msg_id_hex]

            if total_received >= expected_total:
                # all parts received - reassemble in correct order by byte offset
                sorted_offsets = sorted(parts_dict.keys())
                reconstructed = b''.join([parts_dict[offset] for offset in sorted_offsets])
                del self._parts[msg_id_hex]
                del self._lengths[msg_id_hex]
                break

        if not reconstructed:
            # log infos about missing parts for debugging
            parts_dict = self._parts.get(msg_id_hex, {})
            if parts_dict:
                total_received = sum([len(part) for part in parts_dict.values()])
                expected = self._lengths.get(msg_id_hex, 0)
                self.logger.warning(f"Timeout waiting for BLE response of message_id={message_id.value.hex()}. Received {total_received} of expected {expected} bytes in {len(parts_dict)} parts.")
            else:
                self.logger.warning(f"Timeout waiting for BLE response of message_id={message_id.value.hex()}. No parts received.")
            # cleanup leftover parts
            if msg_id_hex in self._parts:
                del self._parts[msg_id_hex]
            if msg_id_hex in self._lengths:
                del self._lengths[msg_id_hex]
            raise TimeoutError(f"No response received for message ID {message_id.value.hex()} within {timeout} seconds.")
        
        return reconstructed

    def add_certificate(self, certificate: str) -> bool:
        """
        Add the aira certificate to allow secure ble communication for commands that require it.

        ### Parameters

        `certificate` : str
            The aira certificate to be added.

        ### Returns

        bool
            True if the certificate was added successfully, False otherwise. Usually will be false if not connected to a device or an invalid certificate is provided.

        ### Examples

        >>> certificate = \"\"\"-----BEGIN CERTIFICATE-----...-----END CERTIFICATE-----\"\"\"
        >>> AiraHome().ble.add_certificate(certificate)
        """
        if not self._ah_i.uuid:
            # No device connected. Please connect to a device before adding a certificate.
            return False
        try:
            self._ah_i.certificate = load_pem_x509_certificate(certificate.encode())
            return True
        except Exception as e:
            return False

    ###
    # Connection methods
    ###

    def is_connected(self) -> bool:
        """
        Check if there is an active BLE connection to a device.

        ### Returns

        bool
            True if connected to a device, False otherwise.

        ### Examples

        >>> AiraHome().ble.is_connected()
        """
        # return False and deletes the client if not connected
        if not self._client:
            return False
        if not self._client.is_connected:
            self._client = None
            return False
        return True

    def discover(self, timeout: int = 5, raw: bool = False) -> dict:
        """
        Returns the list of devices that could be an aira heatpump. NOTICE: Aira is not member of the SIG, therefor it uses company id 0xFFFF which is reserved for development and testing. This means that some discovered devices might not be an actual heatpump.

        ### Parameters

        `timeout` : int, optional
            Timeout for the bluetooth discovery scan in seconds. Defaults to 5 seconds.

        `raw` : bool, optional
            If True, returns the raw discovery cache with BleakDevice objects. Defaults to False.
            
        ### Returns

        list 
            A list contaning discovered devices as dictionaries with their name and address or the raw BleakDevice objects if `raw=True`.

            Example:
            ```
[{'123e4567-e89b-12d3-a456-426614174000': ('AH-123', '12:34:56:78:9A:BC')}]
            ```
        
        ### Examples

        >>> AiraHome().ble.discover(timeout=5, raw=False)
        """

        self.logger.info(f"Starting BLE device discovery (timeout: {timeout}s)")
        
        found_devices = {} # uuid -> (name, address)
        # Discover devices and advertisement data
        self._discovery_cache = {} # reset cache

        try:
            # Start scanning
            self._run_async(self._get_scanner().start)

            self._run_async(asyncio.sleep, timeout) # sleep to allow devices to be discovered
            
            # Stop scanning and process results
            self._run_async(self._get_scanner().stop)
            
            self.logger.info(f"BLE discovery completed. Found {len(self._discovery_cache)} possible candidates.")
            
            if raw:
                return self._discovery_cache
            
            for uuid, device in self._discovery_cache.items():
                found_devices[uuid] = (device.name, device.address)
                self.logger.debug(f"Discovered device: {uuid} - {device.name} ({device.address})")
            
            return found_devices
        except Exception as e:
            self.logger.error(f"BLE discovery failed: {e}", exc_info=True)
            raise

    def connect_uuid(self, uuid: str, timeout: int = 10) -> bool:
        """
        Connect to a device using its UUID.

        ### Parameters

        `uuid` : str
            The UUID of the device to connect to.
        
        `timeout` : int, optional
            Timeout for the bluetooth discovery in seconds. Defaults to 10 seconds.

        ### Returns

        bool
            True if the connection was successful, False otherwise. Usually will be false if the device is not found or cannot be connected to.

        ### Examples

        >>> AiraHome().ble.connect_uuid("123e4567-e89b-12d3-a456-426614174000")
        """
        self.logger.info(f"Attempting to connect to device with UUID: {uuid}")
        
        try:
            devices = self.discover(timeout=timeout, raw=True)
            device = devices.get(uuid, None)
            if not device:
                error_msg = f"Device with UUID {uuid} not found during discovery. To check if the device is close enough, use discover method."
                self.logger.error(error_msg)
                raise BLEDiscoveryError(error_msg)
            
            result = self.connect_device(device, timeout=timeout)
            if result:
                self.logger.info(f"Successfully connected to device {uuid}")
            else:
                self.logger.warning(f"Failed to connect to device {uuid}")
            return result
        except Exception as e:
            error_msg = f"Could not connect to device with UUID {uuid}. Exception: {e}"
            self.logger.error(error_msg, exc_info=True)
            raise BLEConnectionError(error_msg)

    def connect_device(self, device: BLEDevice, timeout: int = 10) -> bool:
        """Connect to a device using a BleakDevice object."""
        self.logger.debug(f"Creating BLE client for device at address: {device.address}")
        
        self._client = BleakClient(device, disconnected_callback=self._on_disconnect)
        if not self._client:
            error_msg = f"Could not create BLE client for device at address {device.address}."
            self.logger.error(error_msg)
            raise BLEConnectionError(error_msg)
        
        try:
            self.logger.debug("Attempting BLE connection...")
            self._run_async(self._client.connect, timeout=timeout)
            if self._client.is_connected:
                # Subscribe to notifications on both characteristics
                self._run_async(self._client.start_notify, char_specifier=self._ah_i.insecure_characteristic, callback=self._on_notify)
                self._run_async(self._client.start_notify, char_specifier=self._ah_i.secure_characteristic, callback=self._on_notify)
                return True
            else:
                self._client = None
                raise BLEConnectionError(f"Could not connect to device at address {device.address}.")
        except Exception as e:
            self._client = None
            raise BLEConnectionError(f"Could not connect to device at address {device.address}. Exception: {e}")

    def connect(self, timeout: int = 10) -> bool:
        """Connect to the device using the cloud defined uuid."""
        if not self._ah_i.uuid:
            raise BLEConnectionError("UUID not set. Please set it before running the automatic connection method.")
        return self.connect_uuid(self._ah_i.uuid, timeout=timeout)

    def get_rssi(self) -> int | None:
        """
        Get the current RSSI (signal strength) of the BLE connection.

        ### Returns

        int | None
            RSSI value in dBm (negative number, closer to 0 is better), or None if not connected.
            Typical values: -50 (excellent) to -100 (very poor)

        ### Examples

        >>> rssi = AiraHome().ble.get_rssi()
        """
        if not self.is_connected():
            return None
        
        rssi = None
        try:
            # This is NOT a public API and may break in future versions of Bleak, we use it here just to have a way to get RSSI. Different platforms may have different implementations, a consistent output is not guaranteed.
            # Tested on Linux (Works), HAOS (Works), Windows (Broken), Mac OS (Works).
            # https://github.com/hbldh/bleak/discussions/879#discussioncomment-3130707
            if hasattr(self._client, '_backend'): 
                if hasattr(self._client._backend, 'get_rssi'): # macos
                    rssi = self._run_async(self._client._backend.get_rssi)
                elif hasattr(self._client._backend, '_device_info'): # linux
                    rssi = self._client._backend._device_info.get('RSSI', None)
                elif hasattr(self._client._backend, '_device'): # ha os
                    rssi = getattr(self._client._backend._device, 'rssi', None)
        except Exception:
            pass

        if isinstance(rssi, int):
            return rssi
        
        if isinstance(rssi, str):
            try:
                return int(rssi)
            except:
                return None
        return None

    def disconnect(self) -> bool:
        """
        Disconnect from the currently connected device. If no device is connected, this method will simply return True.
        
        ### Returns

        bool
            True if disconnected from the device, False otherwise.
        """
        if self.is_connected():
            try:
                self._run_async(self._client.disconnect)
                self._client = None
                self.logger.info("Successfully disconnected from BLE device.")
                return True
            except Exception as e: # if disconnect fails consider the device disconnected
                self._client = None
                self.logger.error(f"Error during disconnection", exc_info=True)
                return False
        else:
            self.logger.debug("No device connected, nothing to disconnect.")
        self._client = None
        return True

    def cleanup(self):
        """Cleanup resources used by the Ble instance."""
        if self.is_connected():
            self.disconnect()

        if self._scanner:
            try:
                self._run_async(self._scanner.stop)
            except Exception as e:
                self.logger.error(f"Error during scanner stop: {e}", exc_info=True)

        self._discovery_cache = {}
        self._parts = {}
        self._lengths = {}
        self._client = None

    ###
    # Heatpump methods
    ###

    def get_data(self, data_type: Enum | int, raw: bool = False) -> dict | Message:
        """
        Sends a GetData request to the connected device and returns the complete response.
        Use `raw=True` to get the raw gRPC response.

        ### Parameters

        `data_type` : Enum | int
            The type of data to request, this can be state, system check state, flow data, wifi networks, configuration, power installation. Use pyairahome.enums.GetDataType.* for values.

        `raw` : bool, optional
            If True, returns the raw gRPC response. Defaults to False.

        ### Returns
    
        dict | DataResponse (Message)
            When `raw=False`: A dictionary containing requested data.
            When `raw=True`: The raw gRPC DataResponse protobuf message.
        
        ### Examples

        >>> from pyairahome.enums import GetDataType
        >>> AiraHome().ble.get_data(data_type=Granularity.DATA_TYPE_STATE, raw=False)
        """
        self.logger.debug(f"Requesting BLE data of type: {data_type}. Attempting to acquire lock.")
        self._run_async(self.lock.acquire)
        self.logger.debug(f"Lock acquired for BLE data request of type: {data_type}.")
        
        try:
            message_id = Uuid1(value=os.urandom(16))
            request = GetData(message_id=message_id,
                              data_type=getattr(data_type, 'value', data_type))
            
            self._send_ble(self._ah_i.insecure_characteristic, request, False)
            response_bytes = self._wait_for_response(message_id)

            # parse the response
            response = DataResponse()
            response.ParseFromString(response_bytes)
            
            self.logger.debug("BLE data request completed successfully")

            if raw:
                return response
            
            return Utils.convert_to_dict(response)
        except Exception as e:
            self.logger.error(f"BLE data request failed for type {data_type}: {e}", exc_info=True)
            raise
        finally:
            self.lock.release()
            self.logger.debug(f"Lock released for BLE data request of type: {data_type}.")

    def get_states(self, raw: bool = False) -> dict | Message:
        """
        Returns the states of the connected device.
        Use `raw=True` to get the raw gRPC response.

        ### Parameters

        `raw` : bool, optional
            If True, returns the raw gRPC response. Defaults to False.

        ### Returns

        dict | State (Message)
            When `raw=False`: A dictionary containing most states for the given device.
            When `raw=True`: The raw gRPC GetDevicesResponse protobuf message.
            
            Example of the expected response content regardless of the `raw` parameter:
            ```
{'state': [{'allowed_pump_mode_state': 'PUMP_MODE_STATE_IDLE',
                       'aws_iot_received_time': datetime.datetime(2025, 9, 23, 7, 17, 57, 122747),
                       'configured_pump_modes': 'PUMP_MODE_STATE_HEATING_COOLING',
                       'cool_curve_deltas': {},
                       'cool_curves': {...},
                       'current_hot_water_temperature': 23.4,
                       'current_outdoor_temperature': 22.5,
                       'current_pump_mode_state': {...}
                       ...]}
            ```
        
        ### Examples

        >>> AiraHome().ble.get_states(raw=False)
        """
        
        return self.get_data(data_type=GetDataType.DATA_TYPE_STATE, raw=raw)

    def get_system_check_state(self, raw: bool = False) -> dict | Message:
        """
        Returns the system check state of the connected device.
        Use `raw=True` to get the raw gRPC response.

        ### Parameters

        `raw` : bool, optional
            If True, returns the raw gRPC response. Defaults to False.

        ### Returns

        dict | SystemCheckState (Message)
            When `raw=False`: A dictionary containing the system check state for the given device.
            When `raw=True`: The raw gRPC SystemCheckState protobuf message.
        
        Example of the expected response content regardless of the `raw` parameter:
            ```
{'system_check_state': {'air_purging': {'state': 'AIR_PURGING_STATE_NOT_STARTED'},
                        'calculated_setpoints': {...},
                        'circulation_pump_status': {},
                        'compressor_speed_test': {'progress': 'PROGRESS_STOPPED'},
                        'energy_balance': {'energy_balance': 2},
                        'energy_calculation': {'current_electrical_power_w': 19,
                                               'current_phase0': 0.3,
                                               ...
                                               'electrical_energy_cum_kwh': 165,
                                               'electrical_energy_cum_wh': 165900,
                                               'voltage_phase0': 242.7,
                                               ...
                                               'water_energy_cum_kwh': 521,
                                               'water_energy_cum_wh': 521830},
                        ...}}
            ```

        ### Examples

        >>> AiraHome().ble.get_system_check_state(raw=False)
        """

        return self.get_data(data_type=GetDataType.DATA_TYPE_SYSTEM_CHECK_STATE, raw=raw)

    def get_flow_data(self, raw: bool = False) -> dict | Message:
        """
        Returns the flow data of the connected device.
        Use `raw=True` to get the raw gRPC response.

        ### Parameters

        `raw` : bool, optional
            If True, returns the raw gRPC response. Defaults to False.

        ### Returns

        dict | FlowData (Message)
            When `raw=False`: A dictionary containing the flow data for the given device.
            When `raw=True`: The raw gRPC FlowData protobuf message.

        Example of the expected response content regardless of the `raw` parameter:
            ```
{'flow_data': {}} # TODO add example response
            ```

        ### Examples

        >>> AiraHome().ble.get_flow_data(raw=False)
        """

        return self.get_data(data_type=GetDataType.DATA_TYPE_FLOW_DATA, raw=raw)

    def get_wifi_networks(self, raw: bool = False) -> dict | Message:
        """
        Returns the wifi networks close to the connected device.
        Use `raw=True` to get the raw gRPC response.

        ### Parameters

        `raw` : bool, optional
            If True, returns the raw gRPC response. Defaults to False.

        ### Returns

        dict | WifiNetworks (Message)
            When `raw=False`: A dictionary containing the wifi networks known to the given device.
            When `raw=True`: The raw gRPC WifiNetworks protobuf message.

        Example of the expected response content regardless of the `raw` parameter:
            ```
{'wifi_networks': {'wifi_networks': [{'mac_address': '00:1A:11:FF:AA:01',
                                      'password_required': True,
                                      'signal_strength': -66,
                                      'ssid': 'Wifi-Name-123'},
                                     ...]}}
            ```

        ### Examples

        >>> AiraHome().ble.get_wifi_networks(raw=False)
        """

        return self.get_data(data_type=GetDataType.DATA_TYPE_WIFI_NETWORKS, raw=raw)

    def get_configuration(self, raw: bool = False) -> dict | Message:
        """
        Returns the configuration of the connected device.
        Use `raw=True` to get the raw gRPC response.

        ### Parameters

        `raw` : bool, optional
            If True, returns the raw gRPC response. Defaults to False.

        ### Returns

        dict | CcvConfig (Message)
            When `raw=False`: A dictionary containing the configuration for the given device.
            When `raw=True`: The raw gRPC CcvConfig protobuf message.

        Example of the expected response content regardless of the `raw` parameter:
            ```
{'config': {'alarm_thresholds': {...},
            'away_mode': {'dhw_tank_temperature_change': -20.0,
                          'room_temperature_change': -3.0},
            'compressor_settings': {'compressor_inner_coil_block_time': 180,
                                    'compressor_limit_time': 3.0,
                                    'dhw_diverting_valve_prerun_time': 15,
                                    ...}
            ...}}
            ```

        ### Examples

        >>> AiraHome().ble.get_configuration(raw=False)
        """

        return self.get_data(data_type=GetDataType.DATA_TYPE_CONFIGURATION, raw=raw)
