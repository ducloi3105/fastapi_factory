import inspect
import importlib
from fastapi.routing import APIRouter
from werkzeug.wrappers.response import Response

from src.common.constants import HTTP_METHODS
from src.common.requestvars import g
from src.bases.error.api import AuthenticationError, MethodNotAllowed

from .method_handler import MethodHandler
from .auth_handler import BaseAuthenticationHandler


class MetaResource(type):
    def __init__(cls, name, bases, attrs):
        super(MetaResource, cls).__init__(name, bases, attrs)
        # the 'methods' module must be defined in the resource directory,
        # all the method handler classes are defined in this module
        methods_module_path = cls.__module__ + '.methods'
        try:
            methods_module = importlib.import_module(methods_module_path)
        except ModuleNotFoundError as e:
            print(name, methods_module_path, e)
            methods_module = None

        if not methods_module:
            return

        method_handlers = attrs.get('method_handlers', {})

        classes = inspect.getmembers(methods_module,
                                     inspect.isclass)

        for cls_name, _class in classes:
            if not issubclass(_class, MethodHandler):
                continue

            if cls_name.upper() not in HTTP_METHODS:
                continue

            method_handlers[cls_name.upper()] = _class

        cls.method_handlers = method_handlers


class APIRouterExtend(APIRouter, metaclass=MetaResource):
    app = None
    request = None
    session = None
    credentials = None
    meta = {}

    # all available methods
    methods = HTTP_METHODS

    # the endpoint of the resource,
    # if this attr is None then this resource
    # will never be registered to the api
    endpoint = None

    # for toggling resource authentication
    auth_required = False

    authentication_handler_class = BaseAuthenticationHandler

    # a dict contains the method handlers of this resource
    method_handlers = {}

    def __init__(self):
        self.session = g().sql_session
        super(APIRouterExtend, self).__init__()

    def _before_auth(self):
        pass

    def _after_auth(self):
        pass

    def _init_method_handler(self, handler_class):
        result = handler_class(
            credentials=self.credentials,
            request=self.request,
            session=self.session,
        )
        return result

    def dispatch_request(self, *args, **kwargs):
        """The main flow of an api resource"""
        # check method available
        print(self.method_handlers)
        method_handler_class = self.method_handlers.get(request.method.upper())

        if not method_handler_class:
            raise MethodNotAllowed

        self._before_auth()

        # check authentication
        authentication_handler = self.authentication_handler_class(
            session=self.session,
            secret_key=self.app.config['SECRET_KEY'],
            request=self.request
        )
        self.credentials = authentication_handler.run()
        if not self.credentials and self.auth_required:
            raise AuthenticationError

        self._after_auth()

        # handle method
        method_handler = self._init_method_handler(
            handler_class=method_handler_class
        )
        response = method_handler.run()

        if not isinstance(response, Response):
            raise Exception('Result must be a Response instance')

        return response


__all__ = (
    'Resource'
)
