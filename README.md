# pyairahome
Python client for Aira Home developed for [AiraHome-Dashboard](https://github.com/Invy55/AiraHome-Dashboard)

## Getting started

### Logging in

```python
from pyairahome import AiraHome
aira = AiraHome()
# login with username and password
aira.login_with_credentials("email_here", "password_here")
# login with tokens
aira.login_with_tokens("id_token_here", "access_token_here", "refresh_token_here")
```

### Retrieving informations:

#### Get devices
Lists heatpumps owned by the user
```python
devices = aira.get_devices()
# {'devices': [{'id': {'value': 'BASE64_ENCODED_ID'}, 'online': {'online': True, 'time': '2025-08-06T15:40:07.549Z'}}]}
```

#### Get device details
Gives details on a specified heatpump
```python
# Ottieni avvenimenti di una giornata
device_id = 'BASE64_ENCODED_ID'
aira.get_device_details(device_id)
# {'heat_pump': {'certificate': {'certificate_pem': '-----BEGIN CERTIFICATE-----\n[...]\n-----END CERTIFICATE-----\n'}, 'id': {'value': 'BASE64_ENCODED_ID'}, 'tank_size': 'WATER_TANK_SIZE_300_LITERS', 'deprecated_tank_size': 'TANK_SIZE_UNSPECIFIED', 'night_mode_enabled': False}}
```
#### Get states
Dumps states of a specified heatpump
```python
# Ottieni avvenimenti di una giornata
device_id = 'BASE64_ENCODED_ID'
aira.get_states(device_id)
# {'heat_pump_states': [{'time': '2025-08-08T21:55:30.541376144Z', 'deprecated_target_indoor_heat': {'temperature': 20.0}, 'target_hot_water_temperature': 50.0, 'current_hot_water_temperature': 65.5, 'heat_pump_id': {'value': 'BASE64_ENCODED_ID'}, 'current_outdoor_temperature': 27.1, [...], 'pump_active_state': 'PUMP_ACTIVE_STATE_IDLE', 'inline_heater_active': False, 'force_heating': {'enabled': False}, 'deprecated_pump_mode_state': 'PUMP_MODE_STATE_UNSPECIFIED', 'away_mode_enabled': False, 'power_preference': 'POWER_PREFERENCE_UNSPECIFIED'}]}
```
#### Send command & stream command
Sends a command to the heatpump and streams the progress/response
```python
command = aira.send_command(device_id, "ping") # {'command_id': {'value': 'SLNXNxTHT8SdNrPvEzvEdw=='}}
for update in aira.stream_command_progress(command['command_id']['value']):
    pass # {'command_progress': {'command_id': {'value': 'SLNXNxTHT8SdNrPvEzvEdw=='}, 'time': '2025-08-08T22:01:19.806295242Z', 'succeeded': {}, 'aws_iot_received_time': '2025-08-08T22:01:19.911289444Z'}}
```

## Help
This project is still a early beta but it should contain everything needed to make it complete, feel free to contribute.

##
#### Disclaimer
_This project is an independent, open-source software library developed for interacting with AiraHome heat pumps via their app gRPC APIs. It is not affiliated with, endorsed by, sponsored by, or associated with AiraHome or any of its subsidiaries, affiliates, or partners. The project is not an official product of AiraHome, and the use of this library does not imply any compatibility, support, or approval from AiraHome. All trademarks, service marks, and company names mentioned herein are the property of their respective owners. Use of this library is at your own risk, and the developers are not responsible for any damages, malfunctions, or issues arising from its use with AiraHome or other heat pump systems._
