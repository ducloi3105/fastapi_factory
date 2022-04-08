from marshmallow import Schema, fields as marshmallow_fields

from src.common.constants import PAGINATION

from .fields import *

STRING_LENGTH_VALIDATORS = {
    'EX_SHORT': lambda value: len(value) <= STRING_LENGTH['EX_SHORT'],
    'SHORT': lambda value: len(value) <= STRING_LENGTH['SHORT'],
    'MEDIUM': lambda value: len(value) <= STRING_LENGTH['MEDIUM'],
    'LONG': lambda value: len(value) <= STRING_LENGTH['LONG'],
    'EX_LONG': lambda value: len(value) <= STRING_LENGTH['EX_LONG'],
    'LARGE': lambda value: len(value) <= STRING_LENGTH['LARGE'],
    'EX_LARGE': lambda value: len(value) <= STRING_LENGTH['EX_LARGE']
}


class BaseSchema(Schema):
    pass


class BaseListingSchema(BaseSchema):
    page = marshmallow_fields.Integer(missing=PAGINATION['page'])
    per_page = marshmallow_fields.Integer(missing=PAGINATION['per_page'])

    sorts = ListField(StringField(validate=STRING_LENGTH_VALIDATORS['LONG']),
                      default=['-created_at'])

    def load(self, data, **kwargs):
        result = super().load(data, **kwargs)
        if not result.get('page'):
            result['page'] = PAGINATION['page']

        if not result.get('per_page'):
            result['per_page'] = PAGINATION['per_page']

        if not result.get('sorts'):
            result['sorts'] = ['-created_at']

        return result
