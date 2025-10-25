"""Cloud API interaction class for Aira Home."""
# cloud.py
from .device.heat_pump.statistics.v1 import service_pb2 as stats_service_pb2, service_pb2_grpc as stats_service_pb2_grpc
from .device.heat_pump.cloud.v1 import service_pb2 as cloud_service_pb2, service_pb2_grpc as cloud_service_pb2_grpc
from .device.heat_pump.command.v1.command_source_pb2 import CommandSource
from .device.heat_pump.command.v1 import command_pb2
from .device.v1 import devices_pb2, devices_pb2_grpc
from grpc import secure_channel, ssl_channel_credentials
from google.protobuf.message import Message
from .util.v1.uuid_pb2 import Uuid as Uuid1
from .commands import CommandBase
from datetime import datetime
from .auth import CognitoAuth
from typing import Generator
from .utils import Utils
from enum import Enum
import os


class Cloud:
    """A client to interact with the Aira Home API using the cloud."""
    
    def __init__(self, airahome_instance):
        """Initialize Cloud with reference to parent AiraHome instance."""
        self._ah_i = airahome_instance
        self.logger = self._ah_i.logger

        self.logger.debug("Initializing Cloud instance")

        # Initialize cognitoauth instance
        self._auth = CognitoAuth(self._ah_i.user_pool_id, self._ah_i.client_id)

        # Initialize gRPC channel and stubs
        channel_options = [                             # Channel options to keep the connection alive
            ('grpc.keepalive_time_ms', 10000),          # Send keepalive ping every 10 seconds
            ('grpc.keepalive_timeout_ms', 5000),        # Wait 5 seconds for keepalive response
            ('grpc.keepalive_permit_without_calls', 1), # Allow keepalive pings without active RPCs
        ]
        self._channel = secure_channel(self._ah_i.aira_backend, ssl_channel_credentials(), options=channel_options)
        self._devices_stub = devices_pb2_grpc.DevicesServiceStub(self._channel)
        self._cloud_service_stub = cloud_service_pb2_grpc.HeatPumpCloudServiceStub(self._channel)
        self._stats_service_stub = stats_service_pb2_grpc.HeatPumpStatisticsServiceStub(self._channel)

    ###
    # Helper methods
    ###

    def _get_id_token(self):
        """Get the ID token from the TokenManager."""
        tokens = self._auth.get_tokens()
        if tokens:
            return tokens.get_id_token()
        return None

    def _get_metadatas(self) -> tuple[tuple[str, str], ...]:
        """Create Metadatas instance with the current settings."""
        id_token = self._get_id_token()
        metadata = (
            ('authorization', f'Bearer {id_token}'),
            ('user-agent', self._ah_i.user_agent),
            ('app-package', self._ah_i.app_package),
            ('app-version', self._ah_i.app_version)
        )
        return metadata

    def call_service(self, stub, method_name: str, request, timeout: int = -1, raw: bool = False) -> Message | dict:
        """Call a gRPC service method with the given request."""
        self.logger.debug(f"Calling gRPC service method: {method_name}")
        
        try:
            # Get the method from the stub dynamically
            method = getattr(stub, method_name)
            if timeout < 0:
                timeout = self._ah_i.grpc_timeout
            
            # Call the method with the request, timeout, and generated metadata
            response = method(
                request,
                timeout=timeout,
                metadata=self._get_metadatas()
            )
            
            self.logger.debug(f"gRPC call {method_name} completed successfully")

            if raw:
                return response
            
            return Utils.convert_to_dict(response)
        except Exception as e:
            self.logger.error(f"gRPC call {method_name} failed: {e}", exc_info=True)
            raise

    def get_tokens(self):
        """Get the TokenManager instance if available."""
        return self._auth.get_tokens()

    ###
    # Auth methods
    ###
    
    def login_with_credentials(self, username: str, password: str):
        """Login using username and password."""
        self.logger.info(f"Attempting login with credentials for user: {username}")
        try:
            result = self._auth.login_credentials(username, password)
            self.logger.info("Login with credentials successful")
            return result
        except Exception as e:
            self.logger.error(f"Login with credentials failed for user {username}: {e}", exc_info=True)
            raise

    def login_with_tokens(self, id_token: str, access_token: str, refresh_token: str):
        """Login using existing tokens."""
        self.logger.info("Attempting login with existing tokens")
        try:
            result = self._auth.login_tokens(id_token, access_token, refresh_token)
            self.logger.info("Login with tokens successful")
            return result
        except Exception as e:
            self.logger.error(f"Login with tokens failed: {e}", exc_info=True)
            raise

    ###
    # Heatpump methods
    ###

    # Heatpump ro methods
    def get_devices(self, raw: bool = False) -> dict | Message:
        """
        Returns the list of devices associated with the authenticated user.
        Use `raw=True` to get the raw gRPC response.

        ### Parameters

        `raw` : bool, optional
            If True, returns the raw gRPC response. Defaults to False.

        ### Returns

        dict | GetDevicesResponse (Message)
            When `raw=False`: A dictionary containing the list of devices with their details.
            When `raw=True`: The raw gRPC GetDevicesResponse protobuf message.
            
            Example of the expected response content regardless of the `raw` parameter:
            ```
{'devices': [{'id': {'value': '123e4567-e89b-12d3-a456-426614174000'},
              'online': {'online': True,
                         'time': datetime.datetime(2025, 9, 18, 19, 40, 22, 363000)}}]}
            ```
        
        ### Examples

        >>> AiraHome().cloud.get_devices(raw=False)
        """
        
        request = devices_pb2.GetDevicesRequest()

        return self.call_service(
            self._devices_stub, 
            "GetDevices", 
            request,
            raw=raw
        )

    def get_device_details(self, device_id: str, raw: bool = False) -> dict | Message: # uuid_format: v1
        """
        Returns the details (including the certificate used for ble) of a specific device by its ID.
        Use `raw=True` to get the raw gRPC response.

        ### Parameters

        `device_id` : str
            Heat pump id in UUID format. E.g., '123e4567-e89b-12d3-a456-426614174000'.

        `raw` : bool, optional
            If True, returns the raw gRPC response. Defaults to False.

        ### Returns

        dict | GetDeviceDetailsResponse (Message)
            When `raw=False`: A dictionary containing some details for the given device.
            When `raw=True`: The raw gRPC GetDevicesResponse protobuf message.
            
            Example of the expected response content regardless of the `raw` parameter:
            ```
{'heat_pump': {'certificate': {'certificate_pem': '-----BEGIN '
                                                  'CERTIFICATE-----\n'
                                                  '...certificate content...\n'
                                                  '-----END '
                                                  'CERTIFICATE-----\n'},
               'id': {'value': '123e4567-e89b-12d3-a456-426614174000'},
               'tank_size': 'WATER_TANK_SIZE_300_LITERS'}}
            ```
        
        ### Examples

        >>> AiraHome().cloud.get_device_details("123e4567-e89b-12d3-a456-426614174000", raw=False)
        """

        _id = Utils.convert_uuid_from_v2(device_id)

        request = devices_pb2.GetDeviceDetailsRequest(id=_id)

        return self.call_service(
            self._devices_stub,
            "GetDeviceDetails",
            request,
            raw=raw
        )

    def get_states(self, device_ids: str | list[str], raw: bool = False) -> dict | Message: # uuid_format: v1
        """
        Returns the states of a specific device by its ID or a list of devices by their IDs.
        Use `raw=True` to get the raw gRPC response.

        ### Parameters

        `device_ids` : str | list[str]
            Heat pump(s) id(s) in UUID format. E.g., '123e4567-e89b-12d3-a456-426614174000'.

        `raw` : bool, optional
            If True, returns the raw gRPC response. Defaults to False.

        ### Returns

        dict | GetStatesResponse (Message)
            When `raw=False`: A dictionary containing most states for the given device.
            When `raw=True`: The raw gRPC GetDevicesResponse protobuf message.
            
            Example of the expected response content regardless of the `raw` parameter:
            ```
{'heat_pump_states': [{'allowed_pump_mode_state': 'PUMP_MODE_STATE_IDLE',
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

        >>> AiraHome().cloud.get_states("123e4567-e89b-12d3-a456-426614174000", raw=False)
        """
        
        if isinstance(device_ids, list):
            heat_pump_ids = []
            for device_id in device_ids:
                heat_pump_ids.append(Utils.convert_uuid_from_v2(device_id))
        else:
            heat_pump_ids = [Utils.convert_uuid_from_v2(device_ids)]

        request = devices_pb2.GetStatesRequest(heat_pump_ids=heat_pump_ids)
        
        return self.call_service(
            self._devices_stub,
            "GetStates",
            request,
            raw=raw
        )

    def get_insights(self,
                     heat_pump_id: str,
                     granularity: Enum | int,
                     start_time: datetime | None = None,
                     end_time: datetime | None = None,
                     raw: bool = False) -> dict | Message: # uuid_format: v2
        """
        Returns insights for a specific heat pump within a given time range. If no time range is provided, it defaults to whatever the backend returns.
        Use `raw=True` to get the raw gRPC response.

        ### Parameters

        `heat_pump_id` : str
            Heat pump id in UUID format. E.g., '123e4567-e89b-12d3-a456-426614174000'.

        `granularity` : Enum | int
            The granularity of the insights, can be unspecified, hourly, daily, monthly. Use pyairahome.enums.Granularity.* for values.

        `start_time` : datetime, optional
            The start time for the insights. If None, defaults to the backend's default.

        `end_time` : datetime, optional
            The end time for the insights. If None, defaults to the backend's default.

        `raw` : bool, optional
            If True, returns the raw gRPC response. Defaults to False.

        ### Returns
    
        dict | GetHeatPumpInsightsResponse (Message)
            When `raw=False`: A dictionary containing insights for the given heat pump.
            When `raw=True`: The raw gRPC GetHeatPumpInsightsResponse protobuf message.
            
            Example of the expected response content regardless of the `raw` parameter:
            ```
{'insights': [{'delivered_heat_wh': 11127.97278440123,
               'energy_consumption_wh': 4900,
               'start_time': {'day': 21, 'month': 9, 'year': 2025}},
              {'delivered_heat_wh': 11529.97278440123,
               'energy_consumption_wh': 3000,
               'start_time': {'day': 22, 'month': 9, 'year': 2025}},
              {'delivered_heat_wh': 436.3242614670768,
               'energy_consumption_wh': 200,
               'start_time': {'day': 23, 'month': 9, 'year': 2025}}]}
            ```
        
        ### Examples

        >>> from pyairahome.enums import Granularity
        >>> AiraHome().cloud.get_insights("123e4567-e89b-12d3-a456-426614174000", granularity=Granularity.GRANULARITY_DAILY, start_time=datetime(2025, 9, 21), end_time=datetime(2025, 9, 23), raw=False)
        """

        if start_time is not None:
            start_time = Utils.datetime_to_localdatetime(start_time)
        if end_time is not None:
            end_time = Utils.datetime_to_localdatetime(end_time)
        
        request = stats_service_pb2.GetHeatPumpInsightsRequest(
            heat_pump_id=Utils.convert_str_to_v2(heat_pump_id),
            start_time=start_time,
            end_time_exclusive=end_time,
            granularity=getattr(granularity, 'value', granularity)
        )

        return self.call_service(
            self._stats_service_stub,
            "GetHeatPumpInsights",
            request,
            raw=raw
        )

    # Heatpump wo methods
    def send_command(self, device_id: str, command_in: CommandBase, timestamp: float | int | None = None, raw: bool = False) -> dict | Message: # uuid_format: v1
        """
        (Use aira.cloud.run_command for convenience)
        Send a command to a specific device by its ID. The command must be one of the supported commands found under pyairahome.commands. Command parameters can be set using the command class instance.
        Use `raw=True` to get the raw gRPC response.

        ### Parameters

        `device_id` : str
            Heat pump id in UUID format. E.g., '123e4567-e89b-12d3-a456-426614174000'.
        
        `command_in` : pyairahome.commands.*
            The command to send. Must be one of the supported commands found under pyairahome.commands.

        `timestamp` : float | int | None, optional
            The timestamp for the command. If None, uses the current time. Can be a float (seconds since epoch), int (seconds since epoch), or datetime object.
        
        `raw` : bool, optional
            If True, returns the raw gRPC response. Defaults to False.

        ### Returns

        dict | SendCommandResponse (Message)
            When `raw=False`: A dictionary containing the result of the command.
            When `raw=True`: The raw gRPC SendCommandResponse protobuf message.
            
            Example of the expected response content regardless of the `raw` parameter:
            ```
{'command_id': {'value': '46ef4514-fe04-deb0-ffd8-7d07156975f2'}}
            ```
        
        ### Examples
        >>> from google.protobuf.duration_pb2 import Duration
        >>> from pyairahome.commands import ActivateHotWaterBoosting
        >>> command_in = ActivateHotWaterBoosting(hot_water_boost_duration=Duration(seconds=3600)) # 1 hour boost
        >>> AiraHome().cloud.send_command("123e4567-e89b-12d3-a456-426614174000", command_in, raw=False)
        """

        heat_pump_id = Utils.convert_uuid_from_v2(device_id)
        
        _time = Utils.convert_to_timestamp(timestamp)

        # Create the command instance dynamically
        command = command_pb2.Command()
        command.command_id.value = os.urandom(16)
        command.time.CopyFrom(_time)
        command.command_source = CommandSource.COMMAND_SOURCE_APP_CONTROL
        # Set the specific command field directly
        field_message = command_in.to_message()
        field_name = command_in.get_field()
        # Merge the field message into the appropriate oneof field
        getattr(command, field_name).MergeFrom(field_message)

        request = cloud_service_pb2.SendCommandRequest(heat_pump_id=heat_pump_id,
                                                       command=command)

        return self.call_service(
            self._cloud_service_stub,
            "SendCommand",
            request,
            raw=raw
        )
    
    # Heatpump stream methods
    def stream_command_progress(self, command_id: str, raw: bool = False) -> Generator[dict | Message, None, None]: # uuid_format: v1
        """
        (Use aira.cloud.run_command for convenience)
        Stream the progress of a command. Returns a generator object that yields updates as they are received until success or failure.
        Use `raw=True` to get the raw gRPC response.

        ### Parameters

        `command_id` : str
            Command id in UUID format. E.g., '46ef4514-fe04-deb0-ffd8-7d07156975f2'.
        
        `raw` : bool, optional
            If True, yields the raw gRPC response. Defaults to False.
        
        ### Yields

        dict | StreamCommandProgressResponse (Message)
            When `raw=False`: A dictionary containing the progress update of the command.
            When `raw=True`: The raw gRPC StreamCommandProgressResponse protobuf message.
            
            Example of the expected response content regardless of the `raw` parameter:
            ```
{'command_progress': {'aws_iot_received_time': datetime.datetime(2025, 9, 26, 15, 38, 49, 214993),
                      'command_id': {'value': '46ef4514-fe04-deb0-ffd8-7d07156975f2'},
                      'succeeded': {},
                      'time': datetime.datetime(2025, 9, 26, 15, 38, 47, 269748)}}
            ```

        ### Examples

        >>> for update in AiraHome().cloud.stream_command_progress("46ef4514-fe04-deb0-ffd8-7d07156975f2", raw=False):
        """

        request = cloud_service_pb2.StreamCommandProgressRequest(command_id=Utils.convert_uuid_from_v2(command_id))

        response = self.call_service(
            self._cloud_service_stub,
            "StreamCommandProgress",
            request,
            raw=True # always raw since we need to map the generator
        )

        if raw:
            return response

        return map(Utils.convert_to_dict, response)

    def run_command(self, device_id: str, command_in: CommandBase, timestamp: float | int | None = None, raw: bool = False) -> Generator[dict | Message, None, None]: # uuid_format: v1
        """
        Run a command and stream its progress until completion. This is a convenience method that combines send_command and stream_command_progress. The command must be one of the supported commands found under pyairahome.commands. Command parameters can be set using the command class instance.
        Use `raw=True` to get the raw gRPC response.
        ### Parameters
        
        `command_in` : pyairahome.commands.*
            The command to send. Must be one of the supported commands found under pyairahome.commands.

        `timestamp` : float | int | None, optional
            The timestamp for the command. If None, uses the current time. Can be a float (seconds since epoch), int (seconds since epoch), or datetime object.
        
        `raw` : bool, optional
            If True, returns the raw gRPC response. Defaults to False.

        ### Yields

        dict | SendCommandResponse (Message)
            When `raw=False`: A dictionary containing the result of the command.
            When `raw=True`: The raw gRPC SendCommandResponse protobuf message.
            
            Example of the expected response content regardless of the `raw` parameter:
            ```
{'command_progress': {'aws_iot_received_time': datetime.datetime(2025, 9, 26, 15, 38, 49, 214993),
                      'command_id': {'value': '46ef4514-fe04-deb0-ffd8-7d07156975f2'},
                      'succeeded': {},
                      'time': datetime.datetime(2025, 9, 26, 15, 38, 47, 269748)}}
            ```
        
        ### Examples
        >>> from google.protobuf.duration_pb2 import Duration
        >>> from pyairahome.commands import ActivateHotWaterBoosting
        >>> command_in = ActivateHotWaterBoosting(hot_water_boost_duration=Duration(seconds=3600)) # 1 hour boost
        >>> AiraHome().cloud.run_command(command_in, raw=False)
        """

        send_response = self.send_command(device_id, command_in, timestamp, raw=False)
        command_id = send_response['command_id']['value']

        def progress_dict_generator():
            last_received = None
            for progress_msg in self.stream_command_progress(command_id=command_id, raw=raw):
                process_dict = Utils.convert_to_dict(progress_msg) if raw else progress_msg

                if last_received is not None:
                    # Compare with last received message
                    if process_dict != last_received:
                        yield process_dict

                last_received = process_dict

        return progress_dict_generator()