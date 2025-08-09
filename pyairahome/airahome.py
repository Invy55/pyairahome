""" Main class for the Aira Home library, providing high-level access to auth and control the heatpump. """
# aira_home.py
from .config import Settings
from .auth import CognitoAuth
from .device.v1 import devices_pb2, devices_pb2_grpc
from .device.heat_pump.cloud.v1 import service_pb2, service_pb2_grpc
from .device.heat_pump.command.v1 import command_pb2
from google.protobuf import timestamp_pb2
from grpc import secure_channel, ssl_channel_credentials
from datetime import datetime
from .utils import Utils, UnknownCommandException

class AiraHome:
    def __init__(self,
                 user_pool_id: str = Settings.USER_POOL_IDS[0],
                 client_id: str = Settings.CLIENT_ID,
                 aira_backend: str = Settings.AIRA_BACKEND,
                 user_agent: str = Settings.USER_AGENT,
                 app_package: str = Settings.APP_PACKAGE,
                 app_version: str = Settings.APP_VERSION):
        """ Initialize the AiraHome instance with user pool ID and client ID. """
        self.user_pool_id = user_pool_id
        self.client_id = client_id
        self._auth = CognitoAuth(self.user_pool_id, self.client_id)
        self.user_agent = user_agent
        self.app_package = app_package
        self.app_version = app_version

        self._channel = secure_channel(aira_backend, ssl_channel_credentials())
        self._devices_stub = devices_pb2_grpc.DevicesServiceStub(self._channel)
        self._services_stub = service_pb2_grpc.HeatPumpCloudServiceStub(self._channel)

    # Auth methods
    def login_with_credentials(self, username: str, password: str):
        """ Login using username and password. """
        return self._auth.login_credentials(username, password)

    def login_with_tokens(self, id_token: str, access_token: str, refresh_token: str):
        """ Login using existing tokens. """
        return self._auth.login_tokens(id_token, access_token, refresh_token)

    def _get_id_token(self):
        """ Get the ID token from the TokenManager. """
        tokens = self._auth.get_tokens()
        if tokens:
            return tokens.get_id_token()
        return None

    def _get_metadatas(self):
        """ Create Metadatas instance with the current settings. """
        id_token = self._get_id_token()
        metadata = (
            ('authorization', f'Bearer {id_token}'),
            ('user-agent', self.user_agent),
            ('app-package', self.app_package),
            ('app-version', self.app_version)
        )
        return metadata

    def get_tokens(self):
        """ Get the TokenManager instance if available. """
        return self._auth.get_tokens()
    
    # Heatpump ro methods
    def get_devices(self, raw: bool = False):
        """ Get the list of devices. """
        response = self._devices_stub.GetDevices(
            devices_pb2.GetDevicesRequest(),
            metadata=self._get_metadatas()
        )
        if raw:
            return response

        return Utils.convert_to_dict(response)

    def get_device_details(self, device_id, raw: bool = False):
        """ Get the details of a specific device. """
        _id = Utils.convert_to_uuid_list(device_id)[0]

        response = self._devices_stub.GetDeviceDetails(
            devices_pb2.GetDeviceDetailsRequest(id=_id),
            metadata=self._get_metadatas()
        )
        if raw:
            return response

        return Utils.convert_to_dict(response)

    def get_states(self, device_ids, raw: bool = False):
        """ Get the states of a specific device. """
        heat_pump_ids = Utils.convert_to_uuid_list(device_ids)

        response = self._devices_stub.GetStates(
            devices_pb2.GetStatesRequest(heat_pump_ids=heat_pump_ids),
            metadata=self._get_metadatas()
        )
        if raw:
            return response

        return Utils.convert_to_dict(response)

    # Heatpump wo methods
    def send_command(self, device_id, command_in, timestamp = None, raw: bool = False, **kwargs):
        """ Send a command to a specific device. """
        heat_pump_id = Utils.convert_to_uuid_list(device_id)[0]
        
        if timestamp is None:
            _time = timestamp_pb2.Timestamp(seconds=0, nanos=0)
        elif isinstance(timestamp, timestamp_pb2.Timestamp):
            _time = timestamp
        elif isinstance(timestamp, int):
            _time = timestamp_pb2.Timestamp(seconds=timestamp, nanos=0)
        elif isinstance(timestamp, datetime):
            _time = timestamp_pb2.Timestamp(seconds=int(timestamp.timestamp()), nanos=0)

        if isinstance(command_in, str) and command_in in Settings.ALLOWED_COMMANDS:
            command_class = type(getattr(command_pb2.Command(), command_in)) # Get the command class dynamically
            command = command_pb2.Command(**{command_in: command_class(**kwargs)}, time=_time) # Create the command instance dynamically
        else:
            raise UnknownCommandException(f"Unknown command: {command_in}. Allowed commands are: {Settings.ALLOWED_COMMANDS}")

        response = self._services_stub.SendCommand(
            service_pb2.SendCommandRequest(heat_pump_id=heat_pump_id,
                                           command=command),
            metadata=self._get_metadatas()
        )
        if raw:
            return response

        return Utils.convert_to_dict(response)
    
    # Heatpump stream methods
    def stream_command_progress(self, command_id, raw: bool = False):
        """ Stream the progress of a command. """
        command_uuid = Utils.convert_to_uuid_list(command_id)[0]

        response = self._services_stub.StreamCommandProgress(
            service_pb2.StreamCommandProgressRequest(command_id=command_uuid),
            metadata=self._get_metadatas()
        )
        if raw:
            return response

        return map(Utils.convert_to_dict, response)

    def stream_states(self, device_ids, raw: bool = False):
        """ Stream the states of a specific device. """
        heat_pump_ids = Utils.convert_to_uuid_list(device_ids)

        response = self._devices_stub.StreamStates(
            devices_pb2.StreamStatesRequest(heat_pump_ids=heat_pump_ids),
            metadata=self._get_metadatas()
        )
        if raw:
            return response

        return map(Utils.convert_to_dict, response)