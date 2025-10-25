"""Commands for interacting with Aira Home devices."""
from .device.heat_pump.command.v1.enable_disable_heating_cooling_pb2 import DisableHeatingFunction as _DisableHeatingFunction, EnableCoolingFunction as _EnableCoolingFunction, EnableHeatingFunction as _EnableHeatingFunction, DisableCoolingFunction as _DisableCoolingFunction
from .device.heat_pump.command.v1.set_inline_heater_ambient_threshold_pb2 import SetInlineHeaterAmbientThreshold as _SetInlineHeaterAmbientThreshold
from .device.heat_pump.command.v1.turn_signature_element_lights_off_pb2 import TurnSignatureElementLightsOff as _TurnSignatureElementLightsOff
from .device.heat_pump.command.v1.clear_scheduled_heat_curve_delta_pb2 import ClearScheduledHeatCurveDeltas as _ClearScheduledHeatCurveDeltas
from .device.heat_pump.command.v1.set_target_hot_water_temperature_pb2 import SetTargetHotWaterTemperature as _SetTargetHotWaterTemperature
from .device.heat_pump.command.v1.turn_signature_element_lights_on_pb2 import TurnSignatureElementLightsOn as _TurnSignatureElementLightsOn
from .device.heat_pump.command.v1.clear_room_supply_setpoint_delta_pb2 import ClearRoomSupplySetpointDelta as _ClearRoomSupplySetpointDelta
from .device.heat_pump.command.v1.activate_night_mode_for_one_hour_pb2 import ActivateNightModeForOneHour as _ActivateNightModeForOneHour
from .device.heat_pump.command.v1.set_outdoor_unit_current_limits_pb2 import SetOutdoorUnitCurrentLimits as _SetOutdoorUnitCurrentLimits
from .device.heat_pump.command.v1.set_scheduled_heat_curve_deltas_pb2 import SetScheduledHeatCurveDeltas as _SetScheduledHeatCurveDeltas
from .device.heat_pump.command.v1.set_heating_cooling_thresholds_pb2 import SetHeatingCoolingThresholds as _SetHeatingCoolingThresholds
from .device.heat_pump.command.v1.set_room_supply_setpoint_delta_pb2 import SetRoomSupplySetpointDelta as _SetRoomSupplySetpointDelta
from .device.heat_pump.command.v1.clear_room_temp_setpoint_delta_pb2 import ClearRoomTempSetpointDelta as _ClearRoomTempSetpointDelta
from .device.heat_pump.command.v1.deactivate_hot_water_boosting_pb2 import DeactivateHotWaterBoosting as _DeactivateHotWaterBoosting
from .device.heat_pump.command.v1.set_energy_balance_thresholds_pb2 import SetEnergyBalanceThresholds as _SetEnergyBalanceThresholds
from .device.heat_pump.command.v1.decommission_wall_thermostat_pb2 import DecommissionWallThermostat as _DecommissionWallThermostat
from .device.heat_pump.command.v1.set_room_temp_setpoint_delta_pb2 import SetRoomTempSetpointDelta as _SetRoomTempSetpointDelta
from .device.heat_pump.command.v1.activate_hot_water_boosting_pb2 import ActivateHotWaterBoosting as _ActivateHotWaterBoosting
from .device.heat_pump.command.v1.set_heat_curve_deltas_pb2 import SetHeatCurveDeltas as _SetHeatCurveDeltas, HeatCurveDeltas
from .device.heat_pump.config.v1.ccv.v1.ccv_config_pb2 import AlarmThresholds, InlineHeater, PumpSpeedSettings, SensorSources
from .device.heat_pump.command.v1.set_cool_curve_deltas_pb2 import SetCoolCurveDeltas as _SetCoolCurveDeltas, CoolCurveDeltas
from .device.heat_pump.command.v1.set_diagnostic_poll_period_pb2 import SetDiagnosticPollPeriod as _SetDiagnosticPollPeriod
from .device.heat_pump.command.v1.reset_legionella_schedule_pb2 import ResetLegionellaSchedule as _ResetLegionellaSchedule
from .device.heat_pump.command.v1.install_app_package_pb2 import InstallApplicationPackage as _InstallApplicationPackage
from .device.heat_pump.command.v1.set_flow_alarm_thresholds_pb2 import SetFlowAlarmThresholds as _SetFlowAlarmThresholds
from .device.heat_pump.command.v1.disable_hot_water_heating_pb2 import DisableHotWaterHeating as _DisableHotWaterHeating
from .device.heat_pump.command.v1.set_zone_setpoints_pb2 import SetZoneSetpoints as _SetZoneSetpoints, ZoneTemperatures
from .device.heat_pump.command.v1.regenerate_thread_config_pb2 import RegenerateThreadConfig as _RegenerateThreadConfig
from .device.heat_pump.command.v1.clear_dhw_setpoint_delta_pb2 import ClearDhwSetpointDelta as _ClearDhwSetpointDelta
from .device.heat_pump.command.v1.enable_hot_water_heating_pb2 import EnableHotWaterHeating as _EnableHotWaterHeating
from .device.heat_pump.command.v1.set_pump_speed_settings_pb2 import SetPumpSpeedSettings as _SetPumpSpeedSettings
from .device.heat_pump.command.v1.set_inline_heater_steps_pb2 import SetInlineHeaterSteps as _SetInlineHeaterSteps
from .device.heat_pump.command.v1.clear_heat_curve_delta_pb2 import ClearHeatCurveDeltas as _ClearHeatCurveDeltas
from .device.heat_pump.command.v1.clear_cool_curve_delta_pb2 import ClearCoolCurveDeltas as _ClearCoolCurveDeltas
from .device.heat_pump.command.v1.set_telemetry_interval_pb2 import SetTelemetryInterval as _SetTelemetryInterval
from .device.heat_pump.command.v1.zone_heating_regulator_pb2 import ZoneHeatingRegulator as _ZoneHeatingRegulator
from .device.heat_pump.config.v1.ccv.v1.heat_curve_pb2 import PiecewiseLinearHeatCurve, PiecewiseLinearCoolCurve
from .device.heat_pump.command.v1.set_dhw_setpoint_delta_pb2 import SetDhwSetpointDelta as _SetDhwSetpointDelta
from .device.heat_pump.command.v1.update_lte_hysteresis_pb2 import UpdateLteHysteresis as _UpdateLteHysteresis
from .device.heat_pump.command.v1.sync_ferroamp_devices_pb2 import SyncFerroampDevices as _SyncFerroampDevices
from .device.heat_pump.command.v1.disable_force_heating_pb2 import DisableForceHeating as _DisableForceHeating
from .device.heat_pump.command.v1.set_wifi_credentials_pb2 import SetWifiCredentials as _SetWifiCredentials
from .device.heat_pump.command.v1.run_legionella_cycle_pb2 import RunLegionellaCycle as _RunLegionellaCycle
from .device.heat_pump.command.v1.unpair_ferroamp_core_pb2 import UnpairFerroampCore as _UnpairFerroampCore
from .device.heat_pump.command.v1.enable_force_heating_pb2 import EnableForceHeating as _EnableForceHeating
from .device.heat_pump.command.v1.set_power_preference_pb2 import SetPowerPreference as _SetPowerPreference
from .device.heat_pump.command.v1.configure_heat_pump_pb2 import ConfigureHeatPump as _ConfigureHeatPump
from .device.heat_pump.command.v1.disable_manual_mode_pb2 import DisableManualMode as _DisableManualMode
from .device.heat_pump.command.v1.configure_time_zone_pb2 import ConfigureTimeZone as _ConfigureTimeZone
from .device.heat_pump.command.v1.acknowledge_errors_pb2 import AcknowledgeErrors as _AcknowledgeErrors
from .device.heat_pump.command.v1.rotate_certificate_pb2 import RotateCertificate as _RotateCertificate
from .device.heat_pump.command.v1.modbus_pb2 import ModbusRequest as _ModbusRequest, ModbusRegisterData
from .device.heat_pump.command.v1.set_sensor_sources_pb2 import SetSensorSources as _SetSensorSources
from .device.heat_pump.command.v1.pair_ferroamp_core_pb2 import PairFerroampCore as _PairFerroampCore
from .device.heat_pump.command.v1.sync_ferroamp_cts_pb2 import SyncFerroampCts as _SyncFerroampCts
from .device.heat_pump.command.v1.install_firmware_pb2 import InstallFirmware as _InstallFirmware
from .device.heat_pump.command.v1.disconnect_wifi_pb2 import DisconnectWiFi as _DisconnectWiFi
from .device.heat_pump.command.v1.remove_schedule_pb2 import RemoveSchedule as _RemoveSchedule
from .device.heat_pump.command.v1.clear_away_mode_pb2 import ClearAwayMode as _ClearAwayMode
from .device.heat_pump.command.v1.set_heat_curves_pb2 import SetHeatCurves as _SetHeatCurves
from .device.heat_pump.command.v1.set_cool_curves_pb2 import SetCoolCurves as _SetCoolCurves
from .device.heat_pump.command.v1.factory_reset_pb2 import FactoryReset as _FactoryReset
from .device.heat_pump.command.v1.update_system_pb2 import UpdateSystem as _UpdateSystem
from .device.heat_pump.command.v1.reboot_device_pb2 import RebootDevice as _RebootDevice
from .device.heat_pump.command.v1.set_away_mode_pb2 import SetAwayMode as _SetAwayMode
from .device.heat_pump.command.v1.update_linux_pb2 import UpdateLinux as _UpdateLinux
from .device.heat_pump.command.v1.add_schedule_pb2 import AddSchedule as _AddSchedule
from .device.heat_pump.command.v1.forbid_lte_pb2 import ForbidLte as _ForbidLte
from .device.heat_pump.command.v1.allow_lte_pb2 import AllowLte as _AllowLte
from .device.heat_pump.command.v1.ping_pb2 import Ping as _Ping
from google._upb._message import RepeatedCompositeContainer
from .device.heat_pump.config.v1.config_pb2 import Config
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.duration_pb2 import Duration
from .schedule.v1.schedule_pb2 import Schedule
from google.protobuf.message import Message
from .util.v1.time_zone_pb2 import TimeZone


class CommandBase:
    """Base class for AiraHome commands. Do **NOT use this class** directly."""
    @property
    def _message(self):
        raise NotImplementedError("You must use a subclass of pyairahome.commands, if you are seeing this message you did something wrong.")

    def get_field(self) -> str:
        return self._field

    def to_message(self) -> Message:
        return self._message
    
    def to_bytes(self) -> bytes:
        return self._message.SerializeToString()

class SetAwayMode(CommandBase):
    """
    `SetAwayMode` command.

    ### Parameters:

    `current_time` : google.protobuf.timestamp_pb2.Timestamp

    `end_time` : google.protobuf.timestamp_pb2.Timestamp

    `target_room_temperature` : builtins.float
    """
    def __init__(self, current_time: Timestamp, end_time: Timestamp, target_room_temperature: float) -> None:
        self._field = "set_away_mode"
        self.current_time = current_time
        self.end_time = end_time
        self.target_room_temperature = target_room_temperature
    
    @property
    def _message(self):
        return _SetAwayMode(current_time=self.current_time, end_time=self.end_time, target_room_temperature=self.target_room_temperature)

class ClearAwayMode(CommandBase):
    """
    `ClearAwayMode` command.
    """
    def __init__(self) -> None:
        self._field = "clear_away_mode"
    
    @property
    def _message(self):
        return _ClearAwayMode()

class ActivateHotWaterBoosting(CommandBase):
    """
    `ActivateHotWaterBoosting` command.

    ### Parameters:

    `hot_water_boost_duration` : google.protobuf.duration_pb2.Duration
    """
    def __init__(self, hot_water_boost_duration: Duration) -> None:
        self._field = "activate_hot_water_boosting"
        self.hot_water_boost_duration = hot_water_boost_duration
    
    @property
    def _message(self):
        return _ActivateHotWaterBoosting(hot_water_boost_duration=self.hot_water_boost_duration)

class DeactivateHotWaterBoosting(CommandBase):
    """
    `DeactivateHotWaterBoosting` command.
    """
    def __init__(self) -> None:
        self._field = "deactivate_hot_water_boosting"
    
    @property
    def _message(self):
        return _DeactivateHotWaterBoosting()

class SetTargetHotWaterTemperature(CommandBase):
    """
    `SetTargetHotWaterTemperature` command.

    ### Parameters:

    `temperature` : builtins.float
    """
    def __init__(self, temperature: float) -> None:
        self._field = "set_target_hot_water_temperature"
        self.temperature = temperature
    
    @property
    def _message(self):
        return _SetTargetHotWaterTemperature(temperature=self.temperature)

class SetWifiCredentials(CommandBase):
    """
    `SetWifiCredentials` command.

    ### Parameters:

    `ssid` : builtins.str

    `password` : builtins.str

    `mac_address` : builtins.str
    """
    def __init__(self, ssid: str, password: str, mac_address: str) -> None:
        self._field = "set_wifi_credentials"
        self.ssid = ssid
        self.password = password
        self.mac_address = mac_address
    
    @property
    def _message(self):
        return _SetWifiCredentials(ssid=self.ssid, password=self.password, mac_address=self.mac_address)

class UpdateLinux(CommandBase):
    """
    `UpdateLinux` command.

    ### Parameters:

    `download_url` : builtins.str

    `sha256` : builtins.bytes
    """
    def __init__(self, download_url: str, sha256: bytes) -> None:
        self._field = "update_linux"
        self.download_url = download_url
        self.sha256 = sha256
    
    @property
    def _message(self):
        return _UpdateLinux(download_url=self.download_url, sha256=self.sha256)

class TurnSignatureElementLightsOn(CommandBase):
    """
    `TurnSignatureElementLightsOn` command.
    """
    def __init__(self) -> None:
        self._field = "turn_signature_element_lights_on"
    
    @property
    def _message(self):
        return _TurnSignatureElementLightsOn()

class TurnSignatureElementLightsOff(CommandBase):
    """
    `TurnSignatureElementLightsOff` command.
    """
    def __init__(self) -> None:
        self._field = "turn_signature_element_lights_off"
    
    @property
    def _message(self):
        return _TurnSignatureElementLightsOff()

class AcknowledgeErrors(CommandBase):
    """
    `AcknowledgeErrors` command.
    """
    def __init__(self) -> None:
        self._field = "acknowledge_errors"
    
    @property
    def _message(self):
        return _AcknowledgeErrors()

class DisconnectWiFi(CommandBase):
    """
    `DisconnectWiFi` command.
    """
    def __init__(self) -> None:
        self._field = "disconnect_wifi"
    
    @property
    def _message(self):
        return _DisconnectWiFi()

class InstallApplicationPackage(CommandBase):
    """
    `InstallApplicationPackage` command.

    ### Parameters:

    `download_url` : builtins.str

    `sha256` : builtins.bytes
    """
    def __init__(self, download_url: str, sha256: bytes) -> None:
        self._field = "install_app_package"
        self.download_url = download_url
        self.sha256 = sha256
    
    @property
    def _message(self):
        return _InstallApplicationPackage(download_url=self.download_url, sha256=self.sha256)

class InstallFirmware(CommandBase):
    """
    `InstallFirmware` command.

    ### Parameters:

    `download_url` : builtins.str

    `sha256` : builtins.bytes

    `firmware_type` : builtins.int

    `thermostat_serial_number` : builtins.str
    """
    def __init__(self, download_url: str, sha256: bytes, firmware_type: int, thermostat_serial_number: str) -> None:
        self._field = "install_firmware"
        self.download_url = download_url
        self.sha256 = sha256
        self.firmware_type = firmware_type
        self.thermostat_serial_number = thermostat_serial_number
    
    @property
    def _message(self):
        return _InstallFirmware(download_url=self.download_url, sha256=self.sha256, firmware_type=self.firmware_type, thermostat_serial_number=self.thermostat_serial_number)

class ConfigureHeatPump(CommandBase):
    """
    `ConfigureHeatPump` command.

    ### Parameters:

    `config` : device.heat_pump.config.v1.config_pb2.Config
    """
    def __init__(self, config: Config) -> None:
        self._field = "configure_heat_pump"
        self.config = config
    
    @property
    def _message(self):
        return _ConfigureHeatPump(config=self.config)

class SetRoomSupplySetpointDelta(CommandBase):
    """
    `SetRoomSupplySetpointDelta` command.

    ### Parameters:

    `room_supply_setpoint_deltas` : google._upb._message.RepeatedCompositeContainer
    """
    def __init__(self, room_supply_setpoint_deltas: RepeatedCompositeContainer) -> None:
        self._field = "set_room_supply_setpoint_delta"
        self.room_supply_setpoint_deltas = room_supply_setpoint_deltas
    
    @property
    def _message(self):
        return _SetRoomSupplySetpointDelta(room_supply_setpoint_deltas=self.room_supply_setpoint_deltas)

class ClearRoomSupplySetpointDelta(CommandBase):
    """
    `ClearRoomSupplySetpointDelta` command.
    """
    def __init__(self) -> None:
        self._field = "clear_room_supply_setpoint_delta"
    
    @property
    def _message(self):
        return _ClearRoomSupplySetpointDelta()

class SetDhwSetpointDelta(CommandBase):
    """
    `SetDhwSetpointDelta` command.

    ### Parameters:

    `dhw_setpoint_deltas` : google._upb._message.RepeatedCompositeContainer
    """
    def __init__(self, dhw_setpoint_deltas: RepeatedCompositeContainer) -> None:
        self._field = "set_dhw_setpoint_delta"
        self.dhw_setpoint_deltas = dhw_setpoint_deltas
    
    @property
    def _message(self):
        return _SetDhwSetpointDelta(dhw_setpoint_deltas=self.dhw_setpoint_deltas)

class ClearDhwSetpointDelta(CommandBase):
    """
    `ClearDhwSetpointDelta` command.
    """
    def __init__(self) -> None:
        self._field = "clear_dhw_setpoint_delta"
    
    @property
    def _message(self):
        return _ClearDhwSetpointDelta()

class RotateCertificate(CommandBase):
    """
    `RotateCertificate` command.

    ### Parameters:

    `download_url` : builtins.str

    `sha256` : builtins.bytes
    """
    def __init__(self, download_url: str, sha256: bytes) -> None:
        self._field = "rotate_certificate"
        self.download_url = download_url
        self.sha256 = sha256
    
    @property
    def _message(self):
        return _RotateCertificate(download_url=self.download_url, sha256=self.sha256)

class FactoryReset(CommandBase):
    """
    `FactoryReset` command.

    ### Parameters:

    `device` : builtins.int
    """
    def __init__(self, device: int) -> None:
        self._field = "factory_reset"
        self.device = device
    
    @property
    def _message(self):
        return _FactoryReset(device=self.device)

class SetHeatCurveDeltas(CommandBase):
    """
    `SetHeatCurveDeltas` command.

    ### Parameters:

    `heat_curve_deltas` : device.heat_pump.command.v1.set_heat_curve_deltas_pb2.HeatCurveDeltas
    """
    def __init__(self, heat_curve_deltas: HeatCurveDeltas) -> None:
        self._field = "set_heat_curve_deltas"
        self.heat_curve_deltas = heat_curve_deltas
    
    @property
    def _message(self):
        return _SetHeatCurveDeltas(heat_curve_deltas=self.heat_curve_deltas)

class ClearHeatCurveDeltas(CommandBase):
    """
    `ClearHeatCurveDeltas` command.

    ### Parameters:

    `clear_zone1` : builtins.bool

    `clear_zone2` : builtins.bool
    """
    def __init__(self, clear_zone1: bool, clear_zone2: bool) -> None:
        self._field = "clear_heat_curve_deltas"
        self.clear_zone1 = clear_zone1
        self.clear_zone2 = clear_zone2
    
    @property
    def _message(self):
        return _ClearHeatCurveDeltas(clear_zone1=self.clear_zone1, clear_zone2=self.clear_zone2)

class SetZoneSetpoints(CommandBase):
    """
    `SetZoneSetpoints` command.

    ### Parameters:

    `zone_setpoints` : device.heat_pump.command.v1.set_zone_setpoints_pb2.ZoneTemperatures

    `kind` : builtins.int
    """
    def __init__(self, zone_setpoints: ZoneTemperatures, kind: int) -> None:
        self._field = "set_zone_setpoints"
        self.zone_setpoints = zone_setpoints
        self.kind = kind
    
    @property
    def _message(self):
        return _SetZoneSetpoints(zone_setpoints=self.zone_setpoints, kind=self.kind)

class Ping(CommandBase):
    """
    `Ping` command.
    """
    def __init__(self) -> None:
        self._field = "ping"
    
    @property
    def _message(self):
        return _Ping()

class SetFlowAlarmThresholds(CommandBase):
    """
    `SetFlowAlarmThresholds` command.

    ### Parameters:

    `alarm_thresholds` : device.heat_pump.config.v1.ccv.v1.ccv_config_pb2.AlarmThresholds
    """
    def __init__(self, alarm_thresholds: AlarmThresholds) -> None:
        self._field = "set_flow_alarm_thresholds"
        self.alarm_thresholds = alarm_thresholds
    
    @property
    def _message(self):
        return _SetFlowAlarmThresholds(alarm_thresholds=self.alarm_thresholds)

class SetOutdoorUnitCurrentLimits(CommandBase):
    """
    `SetOutdoorUnitCurrentLimits` command.

    ### Parameters:

    `compressor_stop` : builtins.float

    `compressor_slow_down` : builtins.float

    `compressor_release` : builtins.float
    """
    def __init__(self, compressor_stop: float, compressor_slow_down: float, compressor_release: float) -> None:
        self._field = "set_outdoor_unit_current_limits"
        self.compressor_stop = compressor_stop
        self.compressor_slow_down = compressor_slow_down
        self.compressor_release = compressor_release
    
    @property
    def _message(self):
        return _SetOutdoorUnitCurrentLimits(compressor_stop=self.compressor_stop, compressor_slow_down=self.compressor_slow_down, compressor_release=self.compressor_release)

class UpdateSystem(CommandBase):
    """
    `UpdateSystem` command.

    ### Parameters:

    `download_url` : builtins.str

    `sha256` : builtins.bytes
    """
    def __init__(self, download_url: str, sha256: bytes) -> None:
        self._field = "update_system"
        self.download_url = download_url
        self.sha256 = sha256
    
    @property
    def _message(self):
        return _UpdateSystem(download_url=self.download_url, sha256=self.sha256)

class SetCoolCurveDeltas(CommandBase):
    """
    `SetCoolCurveDeltas` command.

    ### Parameters:

    `cool_curve_deltas` : device.heat_pump.command.v1.set_cool_curve_deltas_pb2.CoolCurveDeltas
    """
    def __init__(self, cool_curve_deltas: CoolCurveDeltas) -> None:
        self._field = "set_cool_curve_deltas"
        self.cool_curve_deltas = cool_curve_deltas
    
    @property
    def _message(self):
        return _SetCoolCurveDeltas(cool_curve_deltas=self.cool_curve_deltas)

class ClearCoolCurveDeltas(CommandBase):
    """
    `ClearCoolCurveDeltas` command.

    ### Parameters:

    `clear_zone1` : builtins.bool

    `clear_zone2` : builtins.bool
    """
    def __init__(self, clear_zone1: bool, clear_zone2: bool) -> None:
        self._field = "clear_cool_curve_deltas"
        self.clear_zone1 = clear_zone1
        self.clear_zone2 = clear_zone2
    
    @property
    def _message(self):
        return _ClearCoolCurveDeltas(clear_zone1=self.clear_zone1, clear_zone2=self.clear_zone2)

class SetHeatCurves(CommandBase):
    """
    `SetHeatCurves` command.

    ### Parameters:

    `zone1` : device.heat_pump.config.v1.ccv.v1.heat_curve_pb2.PiecewiseLinearHeatCurve

    `zone2` : device.heat_pump.config.v1.ccv.v1.heat_curve_pb2.PiecewiseLinearHeatCurve
    """
    def __init__(self, zone1: PiecewiseLinearHeatCurve, zone2: PiecewiseLinearHeatCurve) -> None:
        self._field = "set_heat_curves"
        self.zone1 = zone1
        self.zone2 = zone2
    
    @property
    def _message(self):
        return _SetHeatCurves(zone1=self.zone1, zone2=self.zone2)

class SetCoolCurves(CommandBase):
    """
    `SetCoolCurves` command.

    ### Parameters:

    `zone1` : device.heat_pump.config.v1.ccv.v1.heat_curve_pb2.PiecewiseLinearCoolCurve

    `zone2` : device.heat_pump.config.v1.ccv.v1.heat_curve_pb2.PiecewiseLinearCoolCurve
    """
    def __init__(self, zone1: PiecewiseLinearCoolCurve, zone2: PiecewiseLinearCoolCurve) -> None:
        self._field = "set_cool_curves"
        self.zone1 = zone1
        self.zone2 = zone2
    
    @property
    def _message(self):
        return _SetCoolCurves(zone1=self.zone1, zone2=self.zone2)

class EnableHeatingFunction(CommandBase):
    """
    `EnableHeatingFunction` command.
    """
    def __init__(self) -> None:
        self._field = "enable_heating_function"
    
    @property
    def _message(self):
        return _EnableHeatingFunction()

class DisableHeatingFunction(CommandBase):
    """
    `DisableHeatingFunction` command.
    """
    def __init__(self) -> None:
        self._field = "disable_heating_function"
    
    @property
    def _message(self):
        return _DisableHeatingFunction()

class EnableCoolingFunction(CommandBase):
    """
    `EnableCoolingFunction` command.
    """
    def __init__(self) -> None:
        self._field = "enable_cooling_function"
    
    @property
    def _message(self):
        return _EnableCoolingFunction()

class DisableCoolingFunction(CommandBase):
    """
    `DisableCoolingFunction` command.
    """
    def __init__(self) -> None:
        self._field = "disable_cooling_function"
    
    @property
    def _message(self):
        return _DisableCoolingFunction()

class ActivateNightModeForOneHour(CommandBase):
    """
    `ActivateNightModeForOneHour` command.
    """
    def __init__(self) -> None:
        self._field = "activate_night_mode_for_one_hour"
    
    @property
    def _message(self):
        return _ActivateNightModeForOneHour()

class RegenerateThreadConfig(CommandBase):
    """
    `RegenerateThreadConfig` command.
    """
    def __init__(self) -> None:
        self._field = "regenerate_thread_config"
    
    @property
    def _message(self):
        return _RegenerateThreadConfig()

class SetDiagnosticPollPeriod(CommandBase):
    """
    `SetDiagnosticPollPeriod` command.

    ### Parameters:

    `poll_period_minutes` : builtins.int
    """
    def __init__(self, poll_period_minutes: int) -> None:
        self._field = "set_diagnostic_poll_period"
        self.poll_period_minutes = poll_period_minutes
    
    @property
    def _message(self):
        return _SetDiagnosticPollPeriod(poll_period_minutes=self.poll_period_minutes)

class EnableHotWaterHeating(CommandBase):
    """
    `EnableHotWaterHeating` command.
    """
    def __init__(self) -> None:
        self._field = "enable_hot_water_heating"
    
    @property
    def _message(self):
        return _EnableHotWaterHeating()

class DisableHotWaterHeating(CommandBase):
    """
    `DisableHotWaterHeating` command.

    ### Parameters:

    `time` : google.protobuf.duration_pb2.Duration
    """
    def __init__(self, time: Duration) -> None:
        self._field = "disable_hot_water_heating"
        self.time = time
    
    @property
    def _message(self):
        return _DisableHotWaterHeating(time=self.time)

class ModbusRequest(CommandBase):
    """
    `ModbusRequest` command.

    ### Parameters:

    `unit` : builtins.int

    `function` : builtins.int

    `address` : builtins.int

    `data` : device.heat_pump.command.v1.modbus_pb2.ModbusRegisterData

    `return_type` : builtins.int
    """
    def __init__(self, unit: int, function: int, address: int, data: ModbusRegisterData, return_type: int) -> None:
        self._field = "modbus_request"
        self.unit = unit
        self.function = function
        self.address = address
        self.data = data
        self.return_type = return_type
    
    @property
    def _message(self):
        return _ModbusRequest(unit=self.unit, function=self.function, address=self.address, data=self.data, return_type=self.return_type)

class RunLegionellaCycle(CommandBase):
    """
    `RunLegionellaCycle` command.
    """
    def __init__(self) -> None:
        self._field = "run_legionella_cycle"
    
    @property
    def _message(self):
        return _RunLegionellaCycle()

class ResetLegionellaSchedule(CommandBase):
    """
    `ResetLegionellaSchedule` command.
    """
    def __init__(self) -> None:
        self._field = "reset_legionella_schedule"
    
    @property
    def _message(self):
        return _ResetLegionellaSchedule()

class DecommissionWallThermostat(CommandBase):
    """
    `DecommissionWallThermostat` command.

    ### Parameters:

    `serial_number` : builtins.str
    """
    def __init__(self, serial_number: str) -> None:
        self._field = "decommission_wall_thermostat"
        self.serial_number = serial_number
    
    @property
    def _message(self):
        return _DecommissionWallThermostat(serial_number=self.serial_number)

class SetHeatingCoolingThresholds(CommandBase):
    """
    `SetHeatingCoolingThresholds` command.

    ### Parameters:

    `ambient_temperature_to_enable_heating_mode` : builtins.float

    `ambient_temperature_to_enable_cooling_mode` : builtins.float
    """
    def __init__(self, ambient_temperature_to_enable_heating_mode: float, ambient_temperature_to_enable_cooling_mode: float) -> None:
        self._field = "set_heating_cooling_thresholds"
        self.ambient_temperature_to_enable_heating_mode = ambient_temperature_to_enable_heating_mode
        self.ambient_temperature_to_enable_cooling_mode = ambient_temperature_to_enable_cooling_mode
    
    @property
    def _message(self):
        return _SetHeatingCoolingThresholds(ambient_temperature_to_enable_heating_mode=self.ambient_temperature_to_enable_heating_mode, ambient_temperature_to_enable_cooling_mode=self.ambient_temperature_to_enable_cooling_mode)

class SetPumpSpeedSettings(CommandBase):
    """
    `SetPumpSpeedSettings` command.

    ### Parameters:

    `settings` : device.heat_pump.config.v1.ccv.v1.ccv_config_pb2.PumpSpeedSettings
    """
    def __init__(self, settings: PumpSpeedSettings) -> None:
        self._field = "set_pump_speed_settings"
        self.settings = settings
    
    @property
    def _message(self):
        return _SetPumpSpeedSettings(settings=self.settings)

class SetInlineHeaterSteps(CommandBase):
    """
    `SetInlineHeaterSteps` command.

    ### Parameters:

    `steps` : device.heat_pump.config.v1.ccv.v1.ccv_config_pb2.InlineHeater
    """
    def __init__(self, steps: InlineHeater) -> None:
        self._field = "set_inline_heater_steps"
        self.steps = steps
    
    @property
    def _message(self):
        return _SetInlineHeaterSteps(steps=self.steps)

class SetSensorSources(CommandBase):
    """
    `SetSensorSources` command.

    ### Parameters:

    `sensors` : device.heat_pump.config.v1.ccv.v1.ccv_config_pb2.SensorSources
    """
    def __init__(self, sensors: SensorSources) -> None:
        self._field = "set_sensor_sources"
        self.sensors = sensors
    
    @property
    def _message(self):
        return _SetSensorSources(sensors=self.sensors)

class SetEnergyBalanceThresholds(CommandBase):
    """
    `SetEnergyBalanceThresholds` command.

    ### Parameters:

    `heating` : builtins.int

    `cooling` : builtins.int
    """
    def __init__(self, heating: int, cooling: int) -> None:
        self._field = "set_energy_balance_thresholds"
        self.heating = heating
        self.cooling = cooling
    
    @property
    def _message(self):
        return _SetEnergyBalanceThresholds(heating=self.heating, cooling=self.cooling)

class DisableManualMode(CommandBase):
    """
    `DisableManualMode` command.
    """
    def __init__(self) -> None:
        self._field = "disable_manual_mode"
    
    @property
    def _message(self):
        return _DisableManualMode()

class RebootDevice(CommandBase):
    """
    `RebootDevice` command.

    ### Parameters:

    `cm` : device.heat_pump.command.v1.reboot_device_pb2.Cm

    `ccv` : device.heat_pump.command.v1.reboot_device_pb2.Ccv
    """
    def __init__(self, cm: _RebootDevice.Cm, ccv: _RebootDevice.Ccv) -> None:
        self._field = "reboot_device"
        self.cm = cm
        self.ccv = ccv
    
    @property
    def _message(self):
        return _RebootDevice(cm=self.cm, ccv=self.ccv)

class SetRoomTempSetpointDelta(CommandBase):
    """
    `SetRoomTempSetpointDelta` command.

    ### Parameters:

    `room_temp_setpoint_deltas` : google._upb._message.RepeatedCompositeContainer
    """
    def __init__(self, room_temp_setpoint_deltas: RepeatedCompositeContainer) -> None:
        self._field = "set_room_temp_setpoint_delta"
        self.room_temp_setpoint_deltas = room_temp_setpoint_deltas
    
    @property
    def _message(self):
        return _SetRoomTempSetpointDelta(room_temp_setpoint_deltas=self.room_temp_setpoint_deltas)

class ClearRoomTempSetpointDelta(CommandBase):
    """
    `ClearRoomTempSetpointDelta` command.
    """
    def __init__(self) -> None:
        self._field = "clear_room_temp_setpoint_delta"
    
    @property
    def _message(self):
        return _ClearRoomTempSetpointDelta()

class SetScheduledHeatCurveDeltas(CommandBase):
    """
    `SetScheduledHeatCurveDeltas` command.

    ### Parameters:

    `heat_curve_deltas` : google._upb._message.RepeatedCompositeContainer
    """
    def __init__(self, heat_curve_deltas: RepeatedCompositeContainer) -> None:
        self._field = "set_scheduled_heat_curve_deltas"
        self.heat_curve_deltas = heat_curve_deltas
    
    @property
    def _message(self):
        return _SetScheduledHeatCurveDeltas(heat_curve_deltas=self.heat_curve_deltas)

class ClearScheduledHeatCurveDeltas(CommandBase):
    """
    `ClearScheduledHeatCurveDeltas` command.
    """
    def __init__(self) -> None:
        self._field = "clear_scheduled_heat_curve_deltas"
    
    @property
    def _message(self):
        return _ClearScheduledHeatCurveDeltas()

class SetTelemetryInterval(CommandBase):
    """
    `SetTelemetryInterval` command.

    ### Parameters:

    `sampling_interval` : google.protobuf.duration_pb2.Duration

    `telemetry_type` : builtins.int
    """
    def __init__(self, sampling_interval: Duration, telemetry_type: int) -> None:
        self._field = "set_telemetry_interval"
        self.sampling_interval = sampling_interval
        self.telemetry_type = telemetry_type
    
    @property
    def _message(self):
        return _SetTelemetryInterval(sampling_interval=self.sampling_interval, telemetry_type=self.telemetry_type)

class AllowLte(CommandBase):
    """
    `AllowLte` command.
    """
    def __init__(self) -> None:
        self._field = "allow_lte"
    
    @property
    def _message(self):
        return _AllowLte()

class ForbidLte(CommandBase):
    """
    `ForbidLte` command.
    """
    def __init__(self) -> None:
        self._field = "forbid_lte"
    
    @property
    def _message(self):
        return _ForbidLte()

class UpdateLteHysteresis(CommandBase):
    """
    `UpdateLteHysteresis` command.

    ### Parameters:

    `delay` : google.protobuf.duration_pb2.Duration
    """
    def __init__(self, delay: Duration) -> None:
        self._field = "update_lte_hysteresis"
        self.delay = delay
    
    @property
    def _message(self):
        return _UpdateLteHysteresis(delay=self.delay)

class ConfigureTimeZone(CommandBase):
    """
    `ConfigureTimeZone` command.

    ### Parameters:

    `time_zone` : util.v1.time_zone_pb2.TimeZone
    """
    def __init__(self, time_zone: TimeZone) -> None:
        self._field = "configure_time_zone"
        self.time_zone = time_zone
    
    @property
    def _message(self):
        return _ConfigureTimeZone(time_zone=self.time_zone)

class SetInlineHeaterAmbientThreshold(CommandBase):
    """
    `SetInlineHeaterAmbientThreshold` command.

    ### Parameters:

    `ambient_temperature_to_allow_inline_heater` : builtins.float
    """
    def __init__(self, ambient_temperature_to_allow_inline_heater: float) -> None:
        self._field = "set_inline_heater_ambient_threshold"
        self.ambient_temperature_to_allow_inline_heater = ambient_temperature_to_allow_inline_heater
    
    @property
    def _message(self):
        return _SetInlineHeaterAmbientThreshold(ambient_temperature_to_allow_inline_heater=self.ambient_temperature_to_allow_inline_heater)

class AddSchedule(CommandBase):
    """
    `AddSchedule` command.

    ### Parameters:

    `schedule` : schedule.v1.schedule_pb2.Schedule
    """
    def __init__(self, schedule: Schedule) -> None:
        self._field = "add_schedule"
        self.schedule = schedule
    
    @property
    def _message(self):
        return _AddSchedule(schedule=self.schedule)

class RemoveSchedule(CommandBase):
    """
    `RemoveSchedule` command.

    ### Parameters:

    `schedule` : schedule.v1.schedule_pb2.Schedule
    """
    def __init__(self, schedule: Schedule) -> None:
        self._field = "remove_schedule"
        self.schedule = schedule
    
    @property
    def _message(self):
        return _RemoveSchedule(schedule=self.schedule)

class PairFerroampCore(CommandBase):
    """
    `PairFerroampCore` command.

    ### Parameters:

    `serial_number` : builtins.str
    """
    def __init__(self, serial_number: str) -> None:
        self._field = "pair_ferroamp_core"
        self.serial_number = serial_number
    
    @property
    def _message(self):
        return _PairFerroampCore(serial_number=self.serial_number)

class ZoneHeatingRegulator(CommandBase):
    """
    `ZoneHeatingRegulator` command.

    ### Parameters:

    `zone1_p` : builtins.float

    `zone1_i` : builtins.float

    `zone2_p` : builtins.float

    `zone2_i` : builtins.float
    """
    def __init__(self, zone1_p: float, zone1_i: float, zone2_p: float, zone2_i: float) -> None:
        self._field = "zone_heating_regulator"
        self.zone1_p = zone1_p
        self.zone1_i = zone1_i
        self.zone2_p = zone2_p
        self.zone2_i = zone2_i
    
    @property
    def _message(self):
        return _ZoneHeatingRegulator(zone1_p=self.zone1_p, zone1_i=self.zone1_i, zone2_p=self.zone2_p, zone2_i=self.zone2_i)

class UnpairFerroampCore(CommandBase):
    """
    `UnpairFerroampCore` command.

    ### Parameters:

    `serial_number` : builtins.str

    `disconnect_wifi` : builtins.bool
    """
    def __init__(self, serial_number: str, disconnect_wifi: bool) -> None:
        self._field = "unpair_ferroamp_core"
        self.serial_number = serial_number
        self.disconnect_wifi = disconnect_wifi
    
    @property
    def _message(self):
        return _UnpairFerroampCore(serial_number=self.serial_number, disconnect_wifi=self.disconnect_wifi)

class SyncFerroampDevices(CommandBase):
    """
    `SyncFerroampDevices` command.
    """
    def __init__(self) -> None:
        self._field = "sync_ferroamp_devices"
    
    @property
    def _message(self):
        return _SyncFerroampDevices()

class SyncFerroampCts(CommandBase):
    """
    `SyncFerroampCts` command.
    """
    def __init__(self) -> None:
        self._field = "sync_ferroamp_cts"
    
    @property
    def _message(self):
        return _SyncFerroampCts()

class EnableForceHeating(CommandBase):
    """
    `EnableForceHeating` command.

    ### Parameters:

    `duration` : google.protobuf.duration_pb2.Duration
    """
    def __init__(self, duration: Duration) -> None:
        self._field = "enable_force_heating"
        self.duration = duration
    
    @property
    def _message(self):
        return _EnableForceHeating(duration=self.duration)

class DisableForceHeating(CommandBase):
    """
    `DisableForceHeating` command.
    """
    def __init__(self) -> None:
        self._field = "disable_force_heating"
    
    @property
    def _message(self):
        return _DisableForceHeating()

class SetPowerPreference(CommandBase):
    """
    `SetPowerPreference` command.

    ### Parameters:

    `power_preference` : builtins.int
    """
    def __init__(self, power_preference: int) -> None:
        self._field = "set_power_preference"
        self.power_preference = power_preference
    
    @property
    def _message(self):
        return _SetPowerPreference(power_preference=self.power_preference)

