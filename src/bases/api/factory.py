import inspect
import sentry_sdk
import os
import importlib
import sys
import time
import types

from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.routing import APIRouter
from werkzeug.exceptions import HTTPException

from src.bases.error.api import HTTPError
from src.common.requestvars import request_global, g
from src.common.utils import log_data

from .resource import Resource


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
        def handle_error(e):
            if isinstance(e, HTTPError):
                status_code = e.status_code
                data = e.output()
            elif isinstance(e, HTTPException):
                status_code = e.code
                data = e.__class__.__name__
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
        if not self.resource_module:
            return

        resource_classes = set()
        rs_root_pack = self.resource_module.__name__.split('.')
        rs_root_dir = os.path.dirname(self.resource_module.__file__)

        if sys.platform == 'linux':
            dir_separator = '/'
        else:
            dir_separator = '\\'

        for dir_path, dir_names, file_names in os.walk(rs_root_dir):
            diff = os.path.relpath(dir_path, rs_root_dir)
            if diff == '.':
                diff_dirs = []
            else:
                diff_dirs = diff.split(dir_separator)
            target_pack_prefix = rs_root_pack + diff_dirs
            for dir_name in dir_names:
                target_pack = target_pack_prefix + [dir_name]
                module = importlib.import_module('.'.join(target_pack))
                classes = inspect.getmembers(module,
                                             inspect.isclass)
                for cls_name, cls in classes:
                    resource_classes.add(cls)

        for cls in resource_classes:
            if not issubclass(cls, Resource):
                continue

            # ignore resources those have none endpoint attr
            if not cls.endpoint:
                continue

            endpoint = cls.endpoint
            # if cls.endpoint_prefix:
            #     endpoint = cls.endpoint_prefix + endpoint
            # print(endpoint, cls.as_view(cls.__name__).__dict__)
            view = cls.as_view(cls.__name__)
            print(view)
            router = APIRouter()
            # router.include_router(
            #     view.router,
            # )
            # app.add_url_rule(endpoint,
            #                  view_func=cls.as_view(cls.__name__))

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
        @app.get("/", include_in_schema=False)
        def redirect_to_docs() -> RedirectResponse:
            return RedirectResponse("/docs")

        '''Callbacks configuration'''
        @app.middleware('http')
        async def add_process_time_header(request: Request, call_next):
            start_time = time.time()
            # self.log_request()

            # init global variable
            initial_g = types.SimpleNamespace()
            request_global.set(initial_g)

            # set connect sql session
            g().sql_session = self.sql_session_factory()

            response = await call_next(request)

            # close connection sql
            g().sql_session.close()
            g().sql_session_factory.remove()

            process_time = time.time() - start_time
            response.headers['X-Process-Time'] = str(process_time)
            return response

        @app.on_event("startup")
        async def connect_to_database() -> None:
            g().sql_session = self.sql_session_factory()

        @app.on_event("shutdown")
        async def shutdown() -> None:
            g().sql_session.close()
            g().sql_session_factory.remove()

        # @app.before_request
        # def handle_before_request():
        #     self.log_request()
        #     g.sql_session = self.sql_session_factory()
        #
        # @app.after_request
        # def handle_after_request(response):
        #     g.sql_session.close()
        #     self.sql_session_factory.remove()
        #     return response

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
