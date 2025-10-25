# PyAiraHome Logging

PyAiraHome includes comprehensive logging for debugging and monitoring purposes. By default, logging is configured with a `NullHandler`, meaning no logs will be output unless you explicitly configure logging.

## Basic Logging Setup

To enable logging output, you can configure the logger before using PyAiraHome:

```python
import logging
from pyairahome import AiraHome

# Configure logging to see all messages
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Or just for PyAiraHome
logger = logging.getLogger('pyairahome')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Now create your AiraHome instance
aira = AiraHome()
```

## Log Levels

PyAiraHome uses the following log levels:

- **DEBUG**: Detailed information for debugging (device discovery details, connection attempts, etc.)
- **INFO**: General information about operations (successful connections, initialization, etc.)
- **WARNING**: Something unexpected happened but the operation can continue
- **ERROR**: A serious problem occurred that prevented an operation from completing

## What Gets Logged

### AiraHome Class
- Instance initialization
- BLE initialization attempts and results

### Cloud Class  
- gRPC service calls and their results
- Authentication attempts (login/logout)
- Connection errors and timeouts

### BLE Class
- Device discovery processes
- Connection/disconnection events
- Data request operations
- UUID parsing and device identification

## Example Log Output

```
2025-10-16 10:30:15 - pyairahome - INFO - AiraHome instance initialized
2025-10-16 10:30:15 - pyairahome - DEBUG - Initializing Cloud instance
2025-10-16 10:30:16 - pyairahome - INFO - Attempting login with credentials for user: user@example.com
2025-10-16 10:30:17 - pyairahome - INFO - Login with credentials successful
2025-10-16 10:30:17 - pyairahome - INFO - Initializing BLE connection
2025-10-16 10:30:17 - pyairahome - DEBUG - Certificate or UUID not available, fetching from cloud
2025-10-16 10:30:17 - pyairahome - DEBUG - Calling gRPC service method: GetDevices
2025-10-16 10:30:18 - pyairahome - DEBUG - gRPC call GetDevices completed successfully
2025-10-16 10:30:18 - pyairahome - DEBUG - Selected device UUID: 12345678-1234-1234-1234-123456789abc
2025-10-16 10:30:18 - pyairahome - INFO - Starting BLE device discovery (timeout: 10s)
2025-10-16 10:30:19 - pyairahome - DEBUG - Discovered potential Aira device: 12345678-1234-1234-1234-123456789abc - AH-001 (AA:BB:CC:DD:EE:FF)
2025-10-16 10:30:28 - pyairahome - INFO - BLE discovery completed. Found 1 devices
2025-10-16 10:30:28 - pyairahome - INFO - BLE connection established successfully
```

## Custom Log Handlers

You can also add custom handlers for specific use cases:

```python
import logging
from pyairahome import AiraHome

# Example: Log only errors to a file
logger = logging.getLogger('pyairahome')
file_handler = logging.FileHandler('aira_errors.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Example: Log everything to console but only warnings+ to file
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

logger.setLevel(logging.DEBUG)

aira = AiraHome()
```