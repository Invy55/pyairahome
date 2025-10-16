"""Main class for the Aira Home library, providing high-level access to auth and heatpump data/controls."""
# airahome.py
from .device.heat_pump.command.v1 import command_pb2
from .utils import CommandUtils, BLEInitializationError
from .config import Settings
from .cloud import Cloud
from .ble import Ble
import asyncio
import logging


class AiraHome:
    def __init__(self,
                 ext_loop: asyncio.AbstractEventLoop | None = None,
                 user_pool_id: str = Settings.USER_POOL_IDS[0],
                 client_id: str = Settings.CLIENT_ID,
                 aira_backend: str = Settings.AIRA_BACKEND,
                 user_agent: str = Settings.USER_AGENT,
                 app_package: str = Settings.APP_PACKAGE,
                 app_version: str = Settings.APP_VERSION,
                 grpc_timeout: int = Settings.GRPC_TIMEOUT,
                 insecure_characteristic: str = Settings.INSECURE_CHARACTERISTIC,
                 secure_characteristic: str = Settings.SECURE_CHARACTERISTIC,
                 default_uuid_selection: int = Settings.DEFAULT_UUID_SELECTION,
                 ble_notify_timeout: int = Settings.BLE_NOTIFY_TIMEOUT,
                 max_ble_chunk_size: int = Settings.MAX_BLE_CHUNK_SIZE):
        # Store configuration for cloud access
        self.user_pool_id = user_pool_id
        self.client_id = client_id
        self.aira_backend = aira_backend
        self.user_agent = user_agent
        self.app_package = app_package
        self.app_version = app_version
        self.grpc_timeout = grpc_timeout
        # Store configuration for ble access
        self.insecure_characteristic = insecure_characteristic
        self.secure_characteristic = secure_characteristic
        self.default_uuid_selection = default_uuid_selection
        self.ble_notify_timeout = ble_notify_timeout
        self.max_ble_chunk_size = max_ble_chunk_size
        
        # Setup logger with NullHandler (no output by default)
        self.logger = logging.getLogger('pyairahome')
        if not self.logger.handlers:
            self.logger.addHandler(logging.NullHandler())
        self.logger.setLevel(logging.DEBUG)  # Allow all levels, let handlers decide
        
        # Initialize cloud instance with reference to this class as parent
        self._cloud = None
        # Initialize ble instance with reference to this class as parent
        self.ext_loop = ext_loop
        self._ble = None

        # Store data needed for simple ble usage
        self.certificate = None
        self.uuid = None

        # Utils
        self._command_list = None
        
        self.logger.info("AiraHome instance initialized")

    @property
    def command_list(self):
        """Get the list of available commands."""
        if not self._command_list:
            self._command_list = self.get_command_list()
        
        return self._command_list

    @property
    def cloud(self):
        """Get the Cloud instance with access to parent AiraHome methods."""
        if self._cloud is None:
            self._cloud = Cloud(self)
        return self._cloud

    @property
    def ble(self):
        """Get the Ble instance with access to parent AiraHome methods."""
        if self._ble is None:
            self._ble = Ble(self, ext_loop=self.ext_loop)
        return self._ble

    ###
    # Internal/Helpers methods
    ###

    def get_command_list(self):
        """Get the list of available commands."""
        commands = []
        supported_commands = command_pb2.Command.DESCRIPTOR.fields_by_name.keys()
        for command in CommandUtils.find_in_modules(Settings.COMMAND_PACKAGE):
            if CommandUtils.camel_case_to_snake_case(command) in supported_commands:
                commands.append(command)
        return commands

    def get_command_fields(self, command: str, raw: bool = False):
        """Get the fields of a specific command."""
        return CommandUtils.get_message_field(command, Settings.COMMAND_PACKAGE, raw=raw)
    
    def init_ble(self) -> bool:
        """Initialize BLE by fetching the certificate and UUID from the cloud."""
        self.logger.info("Initializing BLE connection")
        
        if not self.certificate or not self.uuid:
            self.logger.debug("Certificate or UUID not available, fetching from cloud")
            try:
                devices = self.cloud.get_devices(raw=False)
                if len(devices["devices"])-1 < self.default_uuid_selection:
                    error_msg = f"Default UUID selection index {self.default_uuid_selection} is out of range for available devices ({len(devices['devices'])}). Please adjust using default_uuid_selection parameter when initiating AiraHome class."
                    self.logger.error(error_msg)
                    raise BLEInitializationError(error_msg)
                 
                device = devices["devices"][self.default_uuid_selection]
                self.uuid = device["id"]["value"]
                self.logger.debug(f"Selected device UUID: {self.uuid}")

                device_details = self.cloud.get_device_details(self.uuid, raw=False)
                self.certificate = device_details["heat_pump"]["certificate"]["certificate_pem"]
                self.logger.debug("Certificate retrieved from cloud")

                # try connecting
                connection_result = self.ble.connect()
                if connection_result:
                    self.logger.info("BLE connection established successfully")
                else:
                    self.logger.warning("BLE connection failed")
                return connection_result
            except Exception as e:
                self.logger.error(f"Failed to initialize BLE: {e}", exc_info=True)
                raise
        else:
            self.logger.debug("Certificate and UUID already available, attempting direct connection")
            try:
                connection_result = self.ble.connect()
                if connection_result:
                    self.logger.info("BLE connection established successfully")
                else:
                    self.logger.warning("BLE connection failed")
                return connection_result
            except Exception as e:
                self.logger.error(f"Failed to connect BLE: {e}", exc_info=True)
                raise