import time
import json
import requests
from functools import wraps
from requests.exceptions import ConnectionError, ConnectTimeout

from src.common.json_encoders import CustomJsonEncoder
from src.common.utils import log_data


def request_connection_handler(max_retry=2):
    def decorator(func):
        @wraps(func)
        def handle(*args, **kwargs):
            retry_count = 0
            error = None
            # retry if connection error happens
            while retry_count < max_retry:
                try:
                    response = func(*args, **kwargs)
                    return response

                except (ConnectTimeout,
                        ConnectionError) as e:
                    error = e
                    retry_count += 1
                    time.sleep(retry_count)
            raise error
        return handle
    return decorator


class RequestHandler(object):
    @request_connection_handler(max_retry=2)
    def _do_request(self, method, url, timeout=5000, **kwargs):
        method_handler = getattr(requests, method, None)
        if not method_handler:
            raise Exception('UnsupportedMethod')

        # handle with ObjectId and Datetime
        json_param = kwargs.get('json')
        if json_param:
            kwargs['json'] = json.loads(
                json.dumps(
                    json_param,
                    cls=CustomJsonEncoder,
                )
            )

        log_data(
            mode='info',
            template='{client} - REQUEST - {method} - {url} - {payload}',
            kwargs=dict(
                client=self.__class__.__name__,
                method=method,
                url=url,
                payload=kwargs
            )
        )
        response = method_handler(url=url,
                                  timeout=timeout,
                                  **kwargs)

        log_data(
            mode='info',
            template='{client} - RESPONSE - {method} - {url} - {response}',
            kwargs=dict(
                client=self.__class__.__name__,
                method=method,
                url=url,
                response=response.text
            )
        )
        return response
