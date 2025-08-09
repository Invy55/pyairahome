""" Useful functions """
# utils/utils.py

from google.protobuf.message import Message
from google.protobuf.json_format import MessageToDict
from ..util.v1 import uuid_pb2
from base64 import b64decode
from .exceptions import UnknownTypeException

class Utils:
    @staticmethod
    def convert_to_dict(response: Message):
        """ Convert a protobuf response to a dictionary. """
        return MessageToDict(response,
                             preserving_proto_field_name=True,
                             use_integers_for_enums=False,
                             always_print_fields_with_no_presence=True)

    @staticmethod
    def convert_to_uuid_list(device_ids):
        if isinstance(device_ids, list):
            if all(isinstance(device_id, uuid_pb2.Uuid) for device_id in device_ids):
                heat_pump_ids = device_ids
            elif all(isinstance(device_id, str) for device_id in device_ids):
                heat_pump_ids = [uuid_pb2.Uuid(value=b64decode(str.encode(device_id))) for device_id in device_ids]
            else:
                raise UnknownTypeException(f"Unknown type for {device_ids} list")
        if isinstance(device_ids, uuid_pb2.Uuid): # convert to list if given as single uuid
            heat_pump_ids = [device_ids]
        elif isinstance(device_ids, str): # convert to list of uuids if given in base64
            heat_pump_ids = [uuid_pb2.Uuid(value=b64decode(str.encode(device_ids)))]
        else: # unknown type
            raise UnknownTypeException(f"Unknown type for {device_ids}")

        return heat_pump_ids