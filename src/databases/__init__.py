import json

from redis import Redis as _Redis
from pymongo import MongoClient

from .postgres import Postgres


class Redis(_Redis):
    def get(self, key):
        result = super().get(key)

        if result is None:
            return result

        try:
            result = json.loads(result)
        except json.JSONDecodeError:
            pass
        return result

    def set(self, key, value, **kwargs):

        if not isinstance(value, bytes):
            value = json.dumps(value)

        return super().set(key, value, **kwargs)


class Mongo(MongoClient):
    pass


__all__ = (
    'Postgres',
    'Redis',
    'Mongo'
)
