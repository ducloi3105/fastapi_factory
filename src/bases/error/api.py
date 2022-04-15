from src.bases.error.base import BaseError
from fastapi import HTTPException


class HTTPError(HTTPException):
    status_code = 500

    def __init__(self, detail=None):
        if detail is not None:
            self.detail = detail
        super(HTTPError, self).__init__(self.status_code, self.detail)

    def output(self):
        data = dict(
            status_code=self.status_code,
            detail=self.detail
        )
        return data


class MethodNotAllowed(HTTPError):
    status_code = 405
    detail = 'Method not allowed.'


class AuthenticationError(HTTPError):
    status_code = 401
    detail = 'Authentication error.'


class BadRequestParams(HTTPError):
    status_code = 400
    detail = 'Bad request params.'


class PermissionError(HTTPError):
    status_code = 403
    detail = 'Permission error.'


class ConflictError(HTTPError):
    status_code = 409
    detal = 'Conflict error.'


class ServiceNotAvailable(HTTPError):
    status_code = 503
    detail = 'Service not available.'


class ServerError(HTTPError):
    status_code = 500
    detail = 'Server error.'
