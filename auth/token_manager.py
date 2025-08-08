""" Simple class to manage tokens and their expiration. """
# auth/token_manager.py
from pycognito import Cognito
from ..utils import TokenError

class TokenManager:
    def __init__(self,
                 user_pool_id: str,
                 client_id: str,
                 id_token,
                 access_token,
                 refresh_token):
        """ Initialize the TokenManager with user pool ID, client ID, and tokens. """
        self.u = Cognito(user_pool_id, client_id, id_token=id_token, access_token=access_token, refresh_token=refresh_token)
            
    def verify_tokens(self):
        """ Verify if the tokens are valid. """
        try:
            self.u.verify_tokens()
            return True
        except Exception as e:
            raise TokenError("Token verification failed") from e
    
    def refresh_tokens(self):
        """ Refresh the tokens if they are expired. """
        try:
            self.u.refresh()
            return True
        except Exception as e:
            raise TokenError("Token refresh failed") from e

    def get_id_token(self):
        """ Get the ID token after validating it. """
        try:
            self.verify_tokens()
        except TokenError:
            try:
                self.refresh_tokens()
            except TokenError:
                return None
        return self.u.id_token