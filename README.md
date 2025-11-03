<h3 align="center">PyAiraHome</h3>

<div align="center">

  ![Status](https://img.shields.io/badge/status-active-success)
  [![PyPi](https://img.shields.io/pypi/v/pyairahome)](https://pypi.org/project/pyairahome/)
  [![GitHub Issues](https://img.shields.io/github/issues/invy55/pyairahome)](https://github.com/invy55/pyairahome/issues)
  [![GitHub Pull Requests](https://img.shields.io/github/issues-pr/invy55/pyairahome)](https://github.com/invy55/pyairahome/pulls)
  ![GitHub License](https://img.shields.io/github/license/invy55/pyairahome)
</div>

---

<p align="center"> PyAiraHome is a comprehensive Python library that provides both cloud-based and Bluetooth Low Energy (BLE) connectivity to Aira Home heat pump systems.
    <br> 
</p>

## 📝 Table of Contents
- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [TODO](#todo)
- [Community](#community)
- [Support Me](#supportme)
- [Disclaimer](#disclaimer)

## 🧐 About <a name = "about"></a>
**PyAiraHome** is a comprehensive Python library that enables developers to access Aira Home devices. The library provides seamless integration with Aira's cloud infrastructure via secure **gRPC services**, enabling remote monitoring, control, and data retrieval from anywhere with internet connectivity. Additionally, it offers direct **Bluetooth Low Energy (BLE)** communication for local device interaction, better data coverage and complete with message encryption for secure data exchange.

PyAiraHome features an intuitive **object-oriented API** that supports both raw protobuf responses and convenient Python dictionaries, comprehensive error handling, and detailed type annotations.

## 🏁 Getting Started <a name = "getting_started"></a>
These instructions will get you a copy of the project up and running on your local machine for development. If you prefer an already working system check [AiraHome-Dashboard](https://github.com/invy55/airahome-dashboard) out.

### Prerequisites

- **Internet connection** - Required for cloud-based features and authentication
- **Bluetooth Low Energy (BLE) capability** - Required for local device communication and full data coverage (ensure you're within range of your Aira Brain)

### Installation

Install PyAiraHome directly from PyPI using pip:

```shell
$ pip install pyairahome
```

## 🎈 Usage <a name="usage"></a>

### Quick Start

Here's a basic example showing cloud functionality:

```python
from pyairahome import AiraHome

# Initialize the library
aira = AiraHome()

# Cloud authentication
aira.cloud.login_with_credentials("email@example.com", "password")

# Get device information
devices = aira.cloud.get_devices()
device_id = devices["devices"][0]["id"]["value"]
print(f"Found device: {device_id}")

# Get current device state
states = aira.cloud.get_states(device_id)
print(f"Current temperature: {states['heat_pump_states'][0]['current_hot_water_temperature']}")
```

### Cloud API Examples

#### Authentication and Device Management

```python
# Login with credentials
aira.cloud.login_with_credentials("email@example.com", "password")

# Alternative: Login with existing tokens
# aira.cloud.login_with_tokens("id_token", "access_token", "refresh_token")

# List all devices
devices = aira.cloud.get_devices()
print(f"Found {len(devices['devices'])} devices")

# Get detailed device information
device_details = aira.cloud.get_device_details(device_id)
print(f"Device name: {device_details['name']}")
```

#### Monitoring and Control

```python
# Get current device states
states = aira.cloud.get_states(device_id)
print(states)

# Send commands to device
from pyairahome.commands import Ping
for update in aira.cloud.run_command(device_id, Ping())
    print(f"Command status: {update}")
```

### Bluetooth Low Energy (BLE) Examples

#### Device Discovery and Connection

```python
# Discover nearby Aira devices
devices = aira.ble.discover(timeout=5)
print(f"Found {len(devices)} BLE devices")

# Connect to a specific device by UUID
connected = aira.ble.connect_uuid("your-device-uuid-here")
if connected:
    print("Successfully connected via BLE")
    
    # Get device configuration
    config = aira.ble.get_configuration()
    print(f"Device configuration: {config}")
else:
    print("Failed to connect")
```

#### Working with Raw vs Processed Data

```python
# Get processed data (Python dictionaries)
devices = aira.cloud.get_devices(raw=False)  # Default
print(type(devices))  # <class 'dict'>

# Get raw protobuf data
devices_raw = aira.cloud.get_devices(raw=True)
print(type(devices_raw))  # <class 'pyairahome.device.v1.devices_pb2.GetDevicesResponse'>
```

### Complete Example

```python
from pyairahome import AiraHome
import time

# Initialize and authenticate
aira = AiraHome()
aira.cloud.login_with_credentials("email@example.com", "password")

# Get device information
devices = aira.cloud.get_devices()
if devices["devices"]:
    device_id = devices["devices"][0]["id"]["value"]
    print(f"Working with device: {device_id}")
    
    # Try BLE connection for enhanced data
    try:
        connected = aira.init_ble()
        if connected:
            print("BLE connection established - enhanced data available")
            additional = aira.ble.get_system_check_state()
            print(f"Additional system states: {additional}")
    except Exception as e:
        print(f"BLE connection failed: {e}")
        print("Continuing with cloud-only mode...")
    
    # Monitor device state
    states = aira.cloud.get_states(device_id)
    print(f"Device status: {states}")
    
else:
    print("No devices found")
```

> **Note**: Replace `"email@example.com"` and `"password"` with your actual Aira Home credentials. For BLE functionality, ensure you're within range of your Aira Brain.

## 📋 Todo(s) <a name = "todo"></a>

- [x] Implement BLE commands functionality
- [ ] Replace short comments with more exhaustive ones
- [ ] Create an actual documentation with more examples

Suggestions and contributions are welcome! Feel free to open an issue or pull request with your ideas.

## 🌐 Community <a name = "community"></a>
If you enjoy this project and want to **connect with other users**, we'd love to see you in our community. Come and join us at [airausersforum.com](https://airausersforum.com)!

## ☕ Support me <a name = "supportme"></a>
I created and currently mantain this project because I genuinely enjoy doing so. No need to tip — but if you’d still like to show some appreciation you can do it by clicking on the button below, thank you!

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Y8Y01NUQV3)

## ⚠️ Disclaimer <a name = "disclaimer"></a>

**PyAiraHome** is an independent, open-source software library developed for interacting with Aira Home heat pumps via their app gRPC APIs and Bluetooth Low Energy protocols. This project is **not affiliated with, endorsed by, sponsored by, or associated with** Aira Home or any of its subsidiaries, affiliates, or partners.

### Important Legal Notice

- 🔒 This project is **not an official product** of Aira Home
- ⚖️ Use of this library does **not imply any compatibility, support, or approval** from Aira Home
- 🏷️ All trademarks, service marks, and company names mentioned herein are the **property of their respective owners**
- ⚠️ **Use of this library is at your own risk** - I'm not responsible for any damages, malfunctions, warranty voids, or issues arising from its use
- 🛡️ This software is provided **"AS IS"** without warranty of any kind, express or implied
- 🔍 No proprietary code, trade secrets, or copyrighted materials from Aira Home have been used in the development of this library.

**By using this library, you acknowledge that you understand and accept these terms and any associated risks.**
