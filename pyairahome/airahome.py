"""Main class for the Aira Home library, providing high-level access to auth and heatpump data/controls."""
# airahome.py
from .device.heat_pump.command.v1 import command_pb2
from .utils import CommandUtils, BLEInitializationError
from .config import Settings
from .cloud import Cloud
from .ble import Ble


class AiraHome:
    def __init__(self,
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
        
        # Initialize cloud instance with reference to this class as parent
        self._cloud = None
        # Initialize ble instance with reference to this class as parent
        self._ble = None

        # Store data needed for simple ble usage
        self.certificate = None
        self.uuid = None

        # Utils
        self.command_list = self.get_command_list()

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
            self._ble = Ble(self)
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
        if not self.certificate or not self.uuid:
            devices = self.cloud.get_devices(raw=False)
            if len(devices["devices"])-1 < self.default_uuid_selection:
                raise BLEInitializationError(f"Default UUID selection index {self.default_uuid_selection} is out of range for available devices ({len(devices['devices'])}). Please adjust using default_uuid_selection parameter when initiating AiraHome class.")
             
            device = devices["devices"][self.default_uuid_selection]
            self.uuid = device["id"]["value"]

            device_details = self.cloud.get_device_details(self.uuid, raw=False)
            print(device_details)
            self.certificate = device_details["heat_pump"]["certificate"]["certificate_pem"]

            # try connecting
            return self.ble.connect()
        
        return False