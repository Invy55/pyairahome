"""Custom exceptions for the Aira Home library."""
# utils/exceptions.py


class NotLoggedInException(Exception):
    """Exception raised when a user is not logged in."""
    pass

class AuthenticationError(Exception):
    """Exception raised for authentication errors."""
    pass

class UnknownTypeException(Exception):
    """Exception raised for unknown types."""
    pass

class TokenError(Exception):
    """Exception raised for token errors."""
    pass

class BLEDiscoveryError(Exception):
    """Exception raised for BLE discovery errors."""
    pass

class BLEConnectionError(Exception):
    """Exception raised for BLE connection errors."""
    pass

class BLEInitializationError(Exception):
    """Exception raised for BLE initialization errors."""
    pass