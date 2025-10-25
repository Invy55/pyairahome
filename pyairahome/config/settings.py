"""Class containing default settings for the application."""
# config/settings.py


class Settings:
    USER_POOL_IDS = ["eu-north-1_cnqyjWtbz", "eu-north-1_EyCYO6SAa", "eu-north-1_k0IgmZxLJ"]
    CLIENT_ID = "5eehn0b5d6fsg28rjc5p1u0vi6"
    AIRA_BACKEND = "engagementbff.prod.airahome.com:443"
    USER_AGENT = "AiraApp 1.4.10"
    APP_PACKAGE = "com.airahome.aira"
    APP_VERSION = "1.4.10"
    GRPC_TIMEOUT = 8  # seconds
    COMMAND_PACKAGE = "pyairahome.device.heat_pump.command.v1"
    INSECURE_CHARACTERISTIC = "00000008-0000-a112-a000-a112a0000000"
    SECURE_CHARACTERISTIC = "00000002-0000-a112-a000-a112a0000000"
    DEFAULT_UUID_SELECTION = 0  # 0 = first
    BLE_NOTIFY_TIMEOUT = 8  # seconds
    MAX_BLE_CHUNK_SIZE = 245 # bytes