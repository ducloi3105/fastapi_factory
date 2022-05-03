import sentry_sdk
import os
import importlib
import time
import types

from fastapi import FastAPI, Response, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.bases.error.api import HTTPError
from src.common.logging import log_data
from src.common.context import correlation_id


class Factory(object):
    def __init__(self,
                 sql_session_factory=None,
                 sql_async_session_factory=None,
                 resource_module=None,
                 error_handler=None,
                 request_callback=None,
                 response_callback=None):

        self.sql_session_factory = sql_session_factory
        self.sql_async_session_factory = sql_async_session_factory
        self.resource_module = resource_module
        self.error_handler = error_handler
        self.request_callback = request_callback
        self.response_callback = response_callback

    @staticmethod
    def default_error_handler(app):
        @app.exception_handler(Exception)
        @app.exception_handler(HTTPException)
        async def handle_error(e, response):
            e.state.session.rollback()
            await e.state.async_session.rollback()

            if isinstance(e, HTTPError):
                status_code = e.status_code
                data = e.output()
            elif isinstance(e, HTTPException):
                status_code = e.status_code
                data = e.__class__.__name__
            elif isinstance(e, Request):
                try:
                    status_code = response.status_code
                    data = response.output()
                except:
                    status_code = 500
                    data = dict(detail='Server error')

            else:
                status_code = 500
                data = dict(detail='Server error')

            if status_code >= 500:
                sentry_sdk.capture_exception(e)
                # if app.debug:
                #     raise e
            data['status_code'] = status_code
            return JSONResponse(
                status_code=status_code,
                content=data
            )

    def install_resource(self, app):
        if not self.resource_module:
            return

        rs_root_pack = self.resource_module.__name__.split('.')
        rs_root_dir = os.path.dirname(self.resource_module.__file__)
        for dir_path, dir_names, file_names in os.walk(rs_root_dir):
            diff = os.path.relpath(dir_path, rs_root_dir)
            if diff == '.':
                diff_dirs = []
            else:
                diff_dirs = diff.split('/')
            target_pack_prefix = rs_root_pack + diff_dirs
            for dir_name in dir_names:
                if dir_name == '__pycache__':
                    continue
                target_pack = target_pack_prefix + [dir_name] + ['methods']
                module = importlib.import_module('.'.join(target_pack))
                if hasattr(module, 'router'):
                    app.include_router(module.router)

    def create_app(self, config):
        app = FastAPI(
            title=config.TITLE,
            description=config.DESCRIPTION,
            version=config.VERSION,
            terms_of_service=config.TERMS_OF_SERVICE,
            contact=config.CONTACT,
        )

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
            correlation_id.set(time.time())
            start_time = time.time()
            self.log_request(request)
            # set connect sql session

            request.state.session = self.sql_session_factory()
            request.state.async_session = self.sql_async_session_factory()

            self.before_auth()
            response = await call_next(request)
            self.after_auth()
            # close connection sql
            request.state.session.close()
            await request.state.async_session.close()

            process_time = time.time() - start_time
            response.headers['X-Process-Time'] = str(process_time)
            return response

        '''Resources installation'''
        self.install_resource(app)

        return app

    def before_auth(self):
        pass

    def after_auth(self):
        pass

    @staticmethod
    def log_request(request):
        pattern = '{method} - {endpoint} - {payload}'

        payload = dict(
            body=request.body.__dict__,
            params=request.query_params
        )

        log_data(
            mode='warning',
            template=pattern,
            kwargs=dict(
                endpoint=request.url,
                payload=payload,
                method=request.method
            )
        )
