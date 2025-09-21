""" Main class for the Aira Home library, providing high-level access to auth and control the heatpump. """
# aira_home.py
from .config import Settings
from .auth import CognitoAuth
from .device.v1 import devices_pb2, devices_pb2_grpc
from .device.heat_pump.cloud.v1 import service_pb2 as cloud_service_pb2, service_pb2_grpc as cloud_service_pb2_grpc
from .device.heat_pump.command.v1 import command_pb2
from .device.heat_pump.statistics.v1 import service_pb2 as stats_service_pb2, service_pb2_grpc as stats_service_pb2_grpc
from google.protobuf import timestamp_pb2
from grpc import secure_channel, ssl_channel_credentials
from datetime import datetime
from .utils import Utils, UnknownCommandException, CommandUtils
from .device.heat_pump.command.v1.command_source_pb2 import CommandSource

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
        # Prevent channel closure
        channel_options = [
            ('grpc.keepalive_time_ms', 10000),  # Send keepalive ping every 10 seconds
            ('grpc.keepalive_timeout_ms', 5000),  # Wait 5 seconds for keepalive response
            ('grpc.keepalive_permit_without_calls', 1),  # Allow keepalive pings without active RPCs
        ]
        self._channel = secure_channel(aira_backend, ssl_channel_credentials(), options=channel_options)
        self._devices_stub = devices_pb2_grpc.DevicesServiceStub(self._channel)
        self._cloud_service_stub = cloud_service_pb2_grpc.HeatPumpCloudServiceStub(self._channel)
        self._stats_service_stub = stats_service_pb2_grpc.HeatPumpStatisticsServiceStub(self._channel)

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

    def get_command_list(self):
        """ Get the list of available commands. """
        commands = []
        supported_commands = command_pb2.Command.DESCRIPTOR.fields_by_name.keys()
        for command in CommandUtils.find_in_modules(Settings.COMMAND_PACKAGE):
            if CommandUtils.camel_case_to_snake_case(command) in supported_commands:
                commands.append(command)
        return commands

    def get_command_fields(self, command: str, raw: bool = False):
        """ Get the fields of a specific command. """
        return CommandUtils.get_message_field(command, Settings.COMMAND_PACKAGE, raw=raw)

    def get_tokens(self):
        """ Get the TokenManager instance if available. """
        return self._auth.get_tokens()
    
    # Heatpump ro methods
    def get_devices(self, raw: bool = False):
        """ Get the list of devices. """
        response = self._devices_stub.GetDevices(
            devices_pb2.GetDevicesRequest(),
            metadata=self._get_metadatas(),
            timeout=8
        )
        if raw:
            return response

        return Utils.convert_to_dict(response)

    def get_device_details(self, device_id, raw: bool = False): # uuid_format: v1
        """ Get the details of a specific device. """
        _id = Utils.convert_uuid_from_v2(device_id)

        response = self._devices_stub.GetDeviceDetails(
            devices_pb2.GetDeviceDetailsRequest(id=_id),
            metadata=self._get_metadatas(),
            timeout=8
        )
        if raw:
            return response

        return Utils.convert_to_dict(response)

    def get_states(self, device_ids, raw: bool = False): # uuid_format: v1
        """ Get the states of a specific device. """
        if isinstance(device_ids, list):
            heat_pump_ids = []
            for device_id in device_ids:
                heat_pump_ids.append(Utils.convert_uuid_from_v2(device_id))
        else:
            heat_pump_ids = [Utils.convert_uuid_from_v2(device_ids)]

        response = self._devices_stub.GetStates(
            devices_pb2.GetStatesRequest(heat_pump_ids=heat_pump_ids),
            metadata=self._get_metadatas(),
            timeout=8
        )
        if raw:
            return response

        return Utils.convert_to_dict(response)

    def get_insights(self,
                     heat_pump_id: str,
                     granularity: int,
                     start_time: datetime | None = None,
                     end_time: datetime | None =None,
                     raw: bool = False) -> dict: # uuid_format: v2 # TODO add type of raw response
        """
        Returns insights for a specific heat pump within a given time range. If no time range is provided, it defaults to whatever the backend returns.
        Use `raw=True` to get the raw gRPC response.

        ### Parameters

        `heat_pump_id` : str
            Heat pump id in UUID format. E.g., '123e4567-e89b-12d3-a456-426614174000'.
        `granularity` : int
            The granularity of the insights, can be unspecified, hourly, daily, monthly. Use pyairahome.enums.Granularity.* for values.
        `start_time` : datetime, optional
            The start time for the insights. If None, defaults to the backend's default.
        `end_time` : datetime, optional
            The end time for the insights. If None, defaults to the backend's default.
        `raw` : bool, optional
            If True, returns the raw gRPC response. Defaults to False.
        ### Returns

        #TODO
        
        ### Examples

        >>> from pyairahome.enums import Granularity
        >>> AiraHome().get_insights("123e4567-e89b-12d3-a456-426614174000", granularity=Granularity.GRANULARITY_HOURLY, start_time=datetime(2023, 1, 1), end_time=datetime(2023, 1, 31), raw=False)
        """

        if start_time is not None:
            start_time = Utils.datetime_to_localdatetime(start_time)
        if end_time is not None:
            end_time = Utils.datetime_to_localdatetime(start_time)
        
        response = self._stats_service_stub.GetHeatPumpInsights(
            stats_service_pb2.GetHeatPumpInsightsRequest(heat_pump_id=heat_pump_id, start_time=start_time, end_time_exclusive=end_time, granularity=granularity),
            metadata=self._get_metadatas(),
            timeout=8
        )
        if raw:
            return response

        return Utils.convert_to_dict(response)


    # Heatpump wo methods
    def send_command(self, device_id, command_in, timestamp = None, raw: bool = False, **kwargs): # uuid_format: v1
        """ Send a command to a specific device. """
        heat_pump_id = Utils.convert_uuid_from_v2(device_id)
        
        if timestamp is None:
            _time = timestamp_pb2.Timestamp(seconds=0, nanos=0)
        elif isinstance(timestamp, timestamp_pb2.Timestamp):
            _time = timestamp
        elif isinstance(timestamp, int):
            _time = timestamp_pb2.Timestamp(seconds=timestamp, nanos=0)
        elif isinstance(timestamp, datetime):
            _time = timestamp_pb2.Timestamp(seconds=int(timestamp.timestamp()), nanos=0)
        else:
            _time = timestamp_pb2.Timestamp(seconds=0, nanos=0)

        if isinstance(command_in, str) and command_in in self.get_command_list():
            command_class = type(getattr(command_pb2.Command(), CommandUtils.camel_case_to_snake_case(command_in))) # Get the command class dynamically
            # TODO understand how aira messages (not built-in python types) interact with this
            fields = {field["name"]: field["type"](kwargs[field["name"]]) for field in self.get_command_fields(command_in, raw=True) if field["name"] in kwargs} # Prepare the fields for the command
            command = command_pb2.Command(**{CommandUtils.camel_case_to_snake_case(command_in): command_class(**fields)}, time=_time, command_source=CommandSource.COMMAND_SOURCE_APP_CONTROL) # Create the command instance dynamically
            # source is app since we are using the app endpoints
        else:
            raise UnknownCommandException(f"Unknown command: {command_in}. Allowed commands are: {self.get_command_list()}")

        response = self._cloud_service_stub.SendCommand(
            cloud_service_pb2.SendCommandRequest(heat_pump_id=heat_pump_id,
                                           command=command),
            metadata=self._get_metadatas(),
            timeout=8
        )
        if raw:
            return response

        return Utils.convert_to_dict(response, heat_pump_id)
    
    # Heatpump stream methods
    def stream_command_progress(self, command_id, raw: bool = False):
        """ Stream the progress of a command. """
        command_uuid = Utils.convert_to_uuid_list(command_id)[0]

        response = self._cloud_service_stub.StreamCommandProgress(
            cloud_service_pb2.StreamCommandProgressRequest(command_id=command_uuid),
            metadata=self._get_metadatas(),
            timeout=8
        )
        if raw:
            return response

        return map(Utils.convert_to_dict, response)

    def stream_states(self, device_ids, raw: bool = False): # uuid_format: v1
        """ Stream the states of a specific device. """
        if isinstance(device_ids, list):
            heat_pump_ids = []
            for device_id in device_ids:
                heat_pump_ids.append(Utils.convert_uuid_from_v2(device_id))
        else:
            heat_pump_ids = [Utils.convert_uuid_from_v2(device_ids)]

        response = self._devices_stub.StreamStates(
            devices_pb2.StreamStatesRequest(heat_pump_ids=heat_pump_ids),
            metadata=self._get_metadatas()            
        )
        if raw:
            return response

        for state in response:
            yield Utils.convert_to_dict(state)