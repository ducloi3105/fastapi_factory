import inspect
import sentry_sdk
import os
import importlib
import sys
import time
import types

from fastapi import FastAPI, Response, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.routing import APIRouter
# from werkzeug.exceptions import HTTPException

from src.bases.error.api import HTTPError
from src.common.requestvars import request_global, g
from src.common.utils import log_data


class Factory(object):
    def __init__(self,
                 sql_session_factory=None,
                 resource_module=None,
                 error_handler=None,
                 request_callback=None,
                 response_callback=None):

        self.sql_session_factory = sql_session_factory
        self.resource_module = resource_module
        self.error_handler = error_handler
        self.request_callback = request_callback
        self.response_callback = response_callback

    @staticmethod
    def default_error_handler(app):
        @app.exception_handler(Exception)
        def handle_error(e, response):
            print(1111111, response.status_code, response.output())
            print('222222')

            if isinstance(e, HTTPError):
                status_code = e.status_code
                data = e.output()
            elif isinstance(e, HTTPException):
                status_code = e.code
                data = e.__class__.__name__
            elif isinstance(e, Request):
                status_code = response.status_code
                data = response.output()
            else:
                status_code = 500
                data = dict(message='Server error - %s' % e)

            if status_code >= 500:
                sentry_sdk.capture_exception(e)
                # if app.debug:
                #     raise e
            return JSONResponse(
                status_code=status_code,
                content=data
            )

    def install_resource(self, app):
        return

    def create_app(self):
        app = FastAPI()

        '''Cross origin'''
        origins = [
            'http://localhost.tiangolo.com',
            'https://localhost.tiangolo.com',
            'http://localhost',
            'http://localhost:8080',
            '*'
        ]

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )

        '''Error handling configuration'''
        error_handler = self.error_handler or self.default_error_handler
        error_handler(app)

        '''Include docs'''
        # @app.get("/", include_in_schema=False)
        # def redirect_to_docs() -> RedirectResponse:
        #     return RedirectResponse("/docs")

        '''Callbacks configuration'''
        @app.middleware('http')
        async def add_process_time_header(request: Request, call_next):
            start_time = time.time()
            # self.log_request()

            # init global variable
            initial_g = types.SimpleNamespace()
            request_global.set(initial_g)

            # set connect sql session

            request.state.session = self.sql_session_factory()
            response = await call_next(request)

            # close connection sql
            request.state.session.close()

            process_time = time.time() - start_time
            response.headers['X-Process-Time'] = str(process_time)
            return response

        '''Resources installation'''
        self.install_resource(app)

        return app

    # @staticmethod
    # def log_request():
    #     pattern = 'RECEIVED REQUEST - {method} - {path} - {payload}'
    #
    #     try:
    #         json = request.json
    #     except Exception:
    #         json = {}
    #
    #     payload = dict(
    #         agrs=request.args.to_dict(),
    #         json=json,
    #         form=request.form.to_dict()
    #     )
    #
    #     log_data(
    #         mode='warning',
    #         template=pattern,
    #         kwargs=dict(
    #             path=request.path,
    #             payload=payload,
    #             method=request.method
    #         )
    #     )
