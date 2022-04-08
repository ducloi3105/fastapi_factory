import json
from flask import Response, make_response

from src.bases.schema import BaseSchema
from src.bases.error.api import (AuthenticationError, BadRequestParams,
                                 )
from src.common.json_encoders import CustomJsonEncoder


class MethodHandler(object):
    # HTTP method authentication toggle
    auth_required = False

    permission_requirements = None

    input_schema_class = BaseSchema

    output_handler = None

    raw_params = None

    # request payload
    payload = None

    def __init__(self,
                 app,
                 request,
                 session,
                 credentials=None,
                 **kwargs):
        self.app = app
        self.request = request
        self.session = session
        self.credentials = credentials

        self._check_auth()

        self.payload = self._parse_payload()

    def _fetch_payload(self):
        if self.request.method in ['GET', 'DELETE']:
            payload = self.request.args or {}
        else:
            payload = self.request.json or {}
        return payload.copy()

    def _parse_payload(self):
        schema = self.input_schema_class(unknown='EXCLUDE')

        raw_payload = self._fetch_payload()

        err = schema.validate(raw_payload)
        if err:
            raise BadRequestParams(message=str(err))

        result = schema.load(raw_payload)

        return result

    def handle_logic(self):
        """The main logic of this HTTP method"""
        raise NotImplementedError

    def _check_auth(self):
        if self.auth_required and not self.credentials:
            raise AuthenticationError

    def run(self) -> Response:
        """The main flow of this HTTP method"""

        result = self.handle_logic()

        response = make_response(json.dumps(result,
                                            cls=CustomJsonEncoder), 200)

        response.headers['Content-Type'] = 'application/json'

        return response
