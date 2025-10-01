"""Useful functions for the Aira Home library."""
# utils/utils.py
from google.protobuf.json_format import MessageToDict
from ..util.v1.local_date_time_pb2 import LocalDateTime
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.message import Message
from ..util.v1 import uuid_pb2 as uuid1_pb2
from ..util.v2 import uuid_pb2 as uuid2_pb2
from base64 import b64decode, b64encode
from .exceptions import UnknownTypeException
from datetime import datetime
from uuid import UUID


class Utils:
    @staticmethod
    def convert_to_dict(response: Message) -> dict:
        """Convert a protobuf response to a dictionary. Flattens heatpump id to v2 uuid format. Converts dates to datetime objects."""
        # assume heatpump_id to be v2. if the user uses v1 they should use raw and bypass this function
        # iterate every field and print type and content
        def replace_fields(response):
            # Convert the message to a dictionary for iteration
            response_python = MessageToDict(response, preserving_proto_field_name=True, always_print_fields_with_no_presence=True)

            def process_field(converted, original):
                if isinstance(converted, dict): # process dict
                    for key, value in converted.items():
                        if hasattr(original, key): # ensure the key exists in the original message
                            if isinstance(getattr(original, key), uuid1_pb2.Uuid): # if it's a UUID field
                                # Convert UUID to v2 format
                                converted[key]["value"] = Utils.convert_uuid_to_v2(value['value'])
                            elif isinstance(getattr(original, key), Timestamp): # if it's a Timestamp field
                                # Convert Timestamp to datetime
                                ts = getattr(original, key)
                                converted[key] = ts.ToDatetime()
                            elif isinstance(getattr(original, key), str): # if it's a string it could be date
                                try:
                                    dt = datetime.fromisoformat(value)
                                    converted[key] = dt
                                except ValueError:
                                    pass # not a date string, leave as is
                            else:
                                process_field(value, getattr(original, key)) # recurse into nested dict
                elif isinstance(converted, list):
                    for i in range(len(converted)):
                        process_field(converted[i], original[i])
        
            process_field(response_python, response)
            return response_python
        
        return replace_fields(response)
    
    @staticmethod
    def convert_to_uuid_list(device_ids):
        if isinstance(device_ids, list):
            if all(isinstance(device_id, uuid1_pb2.Uuid) for device_id in device_ids):
                heat_pump_ids = device_ids
            elif all(isinstance(device_id, str) for device_id in device_ids):
                heat_pump_ids = [uuid1_pb2.Uuid(value=b64decode(str.encode(device_id))) for device_id in device_ids]
            else:
                raise UnknownTypeException(f"Unknown type for {device_ids} list")
        elif isinstance(device_ids, uuid1_pb2.Uuid): # convert to list if given as single uuid
            heat_pump_ids = [device_ids]
        elif isinstance(device_ids, str): # convert to list of uuids if given in base64
            heat_pump_ids = [uuid1_pb2.Uuid(value=b64decode(str.encode(device_ids)))]
        else: # unknown type
            raise UnknownTypeException(f"Unknown type [{type(device_ids)}] for {device_ids}")

        return heat_pump_ids
    
    @staticmethod
    def convert_uuid_to_v2(device_id) -> str:
        """Convert a UUID to v2 format"""
        uuid = Utils.convert_to_uuid_list(device_id)[0]
        return str(UUID(uuid.value.hex()))
    
    @staticmethod
    def convert_uuid_from_v2(device_id: str) -> uuid1_pb2.Uuid:
        """Convert a v2 UUID to protobuf format"""
        return uuid1_pb2.Uuid(value=UUID(device_id).bytes)
    
    @staticmethod
    def convert_str_to_v2(device_id: str) -> str:
        """Convert a base64 UUID string to v2 format"""
        return uuid2_pb2.Uuid(value=device_id)
    
    @staticmethod
    def datetime_to_localdatetime(dt):
        return LocalDateTime(year=dt.year, month=dt.month, day=dt.day, hour=dt.hour, minute=dt.minute, second=dt.second, nanos=getattr(dt, "nanos", 0))
    
    @staticmethod
    def convert_to_timestamp(timestamp: float | int | None) -> Timestamp:
        if timestamp is None:
            _time = Timestamp()
            _time.GetCurrentTime()
        elif isinstance(timestamp, Timestamp):
            _time = timestamp
        elif isinstance(timestamp, int):
            _time = Timestamp(seconds=timestamp, nanos=0)
        elif isinstance(timestamp, float): # could have nanos wrong
            seconds, nanos = tuple(map(int, str(timestamp).split(".")))
            _time = Timestamp(seconds=seconds, nanos=nanos)
        elif isinstance(timestamp, datetime):
            seconds, nanos = tuple(map(int, str(timestamp.timestamp()).split(".")))
            _time = Timestamp(seconds=seconds, nanos=nanos)
        else:
            _time = Timestamp(seconds=0, nanos=0)
        return _time