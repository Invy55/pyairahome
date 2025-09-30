from ..device.heat_pump.statistics.v1.service_pb2 import Granularity
from ..device.heat_pump.ble.v1.get_data_pb2 import DataType
from enum import Enum

# Explicitly define __all__ for static analysis
__all__ = ['Granularity', 'GetDataType']

# Convert Protobuf Granularity to Python Enum
Granularity = Enum('Granularity', {
    name: descriptor.number
    for name, descriptor in Granularity.DESCRIPTOR.values_by_name.items()
})

GetDataType = Enum('GetDataType', {
    name: descriptor.number
    for name, descriptor in DataType.DESCRIPTOR.values_by_name.items()
})