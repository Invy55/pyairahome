"""Simple class to manage tokens and their expiration."""
# auth/token_manager.py
from ..utils import TokenError
from pycognito import Cognito


class TokenManager:
    def __init__(self,
                 user_pool_id: str,
                 client_id: str,
                 id_token,
                 access_token,
                 refresh_token):
        """Initialize the TokenManager with user pool ID, client ID, and tokens."""
        self.u = Cognito(user_pool_id, client_id, id_token=id_token, access_token=access_token, refresh_token=refresh_token)
            
    def verify_tokens(self):
        """Verify if the tokens are valid."""
        try:
            self.u.verify_tokens()
            return True
        except Exception as e:
            raise TokenError("Token verification failed") from e
    
    def refresh_tokens(self):
        """Refresh the tokens if they are expired."""
        try:
            self.u.check_token()
            return True
        except Exception as e:
            raise TokenError("Token refresh failed") from e

    def get_id_token(self):
        """Get the ID token after validating it."""
        try:
            self.refresh_tokens()
        except TokenError:
            return None
        return self.u.id_token

    def dict(self):
        """Get a dictionary representation of the tokens."""
        return {
            "id_token": self.get_id_token(),
            "access_token": self.u.access_token,
            "refresh_token": self.u.refresh_token
        }