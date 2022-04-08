import json
from datetime import datetime


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, o: any) -> any:
        if isinstance(o, datetime):
            return o.isoformat()
        return super(CustomJsonEncoder, self).default(o)
