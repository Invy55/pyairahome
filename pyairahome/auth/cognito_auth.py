"""Simple class to login with cognito and load tokens in the TokenManager class."""
# auth/cognito_auth.py

from pycognito import Cognito
from .token_manager import TokenManager
from ..utils import AuthenticationError, NotLoggedInException

class CognitoAuth:
    def __init__(self,
                 user_pool_id :str,
                 client_id :str):
        """Initialize the CognitoAuth with user pool ID, client ID. Allows logging in and creating a TokenManager."""
        self.user_pool_id = user_pool_id
        self.client_id = client_id
        self._tokens = None

    def login_credentials(self, username: str, password: str):
        """Login using username and password. Returns a TokenManager instance"""	
        try:
            user = Cognito(self.user_pool_id, self.client_id, username=username)
            user.authenticate(password=password)
            self._tokens = TokenManager(
                user_pool_id=self.user_pool_id,
                client_id=self.client_id,
                id_token=user.id_token,
                access_token=user.access_token,
                refresh_token=user.refresh_token
            )
            self._tokens.verify_tokens()
            return self._tokens
        except Exception as e:
            raise AuthenticationError("Login failed while attempting to login with username and password") from e

    def login_tokens(self, id_token: str, access_token: str, refresh_token: str):
        """Login using existing tokens. Returns a TokenManager instance"""
        try:
            self._tokens = TokenManager(
                user_pool_id=self.user_pool_id,
                client_id=self.client_id,
                id_token=id_token,
                access_token=access_token,
                refresh_token=refresh_token
            )
            self._tokens.verify_tokens()
            return self._tokens
        except Exception as e:
            raise AuthenticationError("Login failed while attempting to login with tokens") from e

    def get_tokens(self):
        """Get the TokenManager instance if available."""
        if self._tokens is None:
            raise NotLoggedInException("Please login before doing anything else")
        self._tokens.refresh_tokens() # verify and refresh the tokens before using them
        return self._tokens

