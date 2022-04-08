from src.bases.error.api import ServerError
from src.bases.error.service import ServiceError


class AuthenticationHandler(object):
    def __init__(self, request, session, secret_key):
        self.request = request
        self.session = session
        self.secret_key = secret_key

    def run(self):
        """Return User or None"""
        raise NotImplementedError


class BaseAuthenticationHandler(AuthenticationHandler):
    def run(self):
        auth_data = self.request.headers.get('Authorization', None)
        if not auth_data:
            return None

        try:
            bearer, access_token = auth_data.split(' ')
        except ValueError:
            return None

        if bearer != 'Bearer' or not access_token:
            return None

        raise Exception('ImplementAuthentication')
        credentials = dict()
        return credentials
