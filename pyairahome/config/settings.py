""" Class containing default settings for the application. """
# config/settings.py

class Settings:
    USER_POOL_IDS = ["eu-north-1_cnqyjWtbz", "eu-north-1_EyCYO6SAa", "eu-north-1_k0IgmZxLJ"]
    CLIENT_ID = "5eehn0b5d6fsg28rjc5p1u0vi6"
    AIRA_BACKEND = "engagementbff.prod.airahome.com:443"
    USER_AGENT = "AiraApp 1.4.7"
    APP_PACKAGE = "com.airahome.aira"
    APP_VERSION = "1.4.7"
    ALLOWED_COMMANDS = ["set_zone_setpoints", "set_away_mode", "clear_away_mode", "activate_hot_water_boosting", "deactivate_hot_water_boosting", "activate_night_mode_for_one_hour", "set_target_hot_water_temperature", "set_wifi_credentials", "update_linux", "rotate_certificate", "turn_signature_element_lights_on", "turn_signature_element_lights_off", "acknowledge_errors", "disconnect_wifi", "install_app_package", "install_firmware", "configure_heat_pump", "configure_time_zone", "factory_reset", "set_heat_curve_deltas", "clear_heat_curve_delta", "ping", "set_flow_alarm_thresholds", "set_outdoor_unit_current_limits", "set_cool_curve_deltas", "clear_cool_curve_delta", "update_system", "set_heat_curves", "set_cool_curves", "regenerate_thread_config", "set_diagnostic_poll_period", "enable_hot_water_heating", "disable_hot_water_heating", "modbus", "run_legionella_cycle", "reset_legionella_schedule", "decommission_wall_thermostat", "set_heating_cooling_thresholds", "set_pump_speed_settings", "set_inline_heater_steps", "set_sensor_sources", "set_energy_balance_thresholds", "disable_manual_mode", "reboot_device", "set_scheduled_heat_curve_deltas", "clear_scheduled_heat_curve_deltas", "set_telemetry_interval", "allow_lte", "forbid_lte", "update_lte_hysteresis", "set_inline_heater_ambient_threshold", "add_schedule", "remove_schedule", "pair_ferroamp_core", "zone_heating_regulator", "unpair_ferroamp_core", "sync_ferroamp_devices", "sync_ferroamp_cts", "enable_force_heating", "disable_force_heating", "set_power_preference"]