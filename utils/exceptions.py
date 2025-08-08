# exceptions/exceptions.py

class NotLoggedInException(Exception):
    """ Exception raised when a user is not logged in. """
    pass

class AuthenticationError(Exception):
    """ Exception raised for authentication errors. """
    pass

class UnknownTypeException(Exception):
    """ Exception raised for unknown types. """
    pass

class UnknownCommandException(Exception):
    """ Exception raised for unknown commands. """
    pass

class TokenError(Exception):
    """ Exception raised for token errors. """
    pass

