import json


class BaseError(Exception):
    error = None
    detail = 'An unknown error happened.'

    def __init__(self, error=None, detail=None, meta=None):
        if detail:
            self.detail = detail

        if error:
            self.error = error
        else:
            self.error = self.__class__.__name__

        self.meta = meta

    def output(self):
        data = {
            'detail': self.detail,
            'error': self.error
        }
        if self.meta:
            data['meta'] = self.meta
        return data

    def __str__(self):
        return json.dumps(self.output())

