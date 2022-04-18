import logging
import inspect
from .context import correlation_id

log = logging.getLogger('WEBMAIL')

formatter = logging.Formatter('%(asctime)-15s %(levelname)s '
                              # '%(clientip)s '
                              '%(correlation_id)s %(message)s')


class ContextFilter(logging.Filter):
    """"Provides correlation id parameter for the logger"""

    def filter(self, record):
        record.correlation_id = correlation_id.get()
        return True


ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)
log.addFilter(ContextFilter())


def make_loggable_data(data):
    length = 1000
    result = str(data)

    if len(result) > length:
        result = result[:length] + '...'

    return result


def log_data(mode: str,
             template: str = None,
             args: list = None,
             kwargs: dict = None):
    handler = getattr(log, mode)
    if not args:
        args = []
    if not kwargs:
        kwargs = {}

    _args = [
        make_loggable_data(i)
        for i in args
    ]

    _kwargs = dict(list(map(
        lambda i: (i[0], make_loggable_data(i[1])),
        kwargs.items()
    )))

    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    template = f'{template} - {module.__name__}'
    handler(template.format(*_args, **_kwargs))
