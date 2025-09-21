from enum import Enum
from ..device.heat_pump.statistics.v1.service_pb2 import Granularity

# Explicitly define __all__ for static analysis
__all__ = ['Granularity']

# Convert Protobuf Granularity to Python Enum
Granularity = Enum('Granularity', {
    name: descriptor.number
    for name, descriptor in Granularity.DESCRIPTOR.values_by_name.items()
})