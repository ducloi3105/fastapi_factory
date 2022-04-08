import re
import json
from marshmallow import fields, ValidationError
from datetime import datetime
from werkzeug.datastructures import FileStorage
from werkzeug.wsgi import LimitedStream

from src.common.constants import STRING_LENGTH, PHONE_REGEX


class StringField(fields.String):
    def _serialize(self, value, attr=None, data=None, **kwargs):
        value = super()._deserialize(value, attr=None, data=None, **kwargs)
        if value:
            value = value.strip()
        return value


class IdField(StringField):
    def _validate(self, value):
        super()._validate(value)
        if len(value) != STRING_LENGTH['UUID4']:
            raise ValidationError('Invalid id.')


class PhoneField(StringField):
    def _validate(self, value):
        super()._validate(value)
        if not re.compile(PHONE_REGEX).match(value):
            raise ValidationError('Invalid phone.')


class DatetimeField(fields.DateTime):
    def _validate(self, value):
        if not isinstance(value, datetime):
            if isinstance(value, (float, int)):
                try:
                    value = datetime.fromtimestamp(value)
                except Exception:
                    raise ValidationError('Invalid datetime!')
        return super()._validate(value)

    def _deserialize(self, value, attr=None, data=None, **kwargs):
        if isinstance(value, (str, int)):
            try:
                value = float(value)
            except ValueError:
                pass

        if isinstance(value, str) and not value:
            if self.allow_none:
                value = None

        if isinstance(value, float):
            value = datetime.fromtimestamp(value)
        return super()._deserialize(value, attr, data, **kwargs)


class FileField(fields.Field):
    def _validate(self, value):
        if not isinstance(value, FileStorage):
            raise ValidationError('Invalid file.')


class StreamField(fields.Field):
    def _validate(self, value):
        if not isinstance(value, LimitedStream):
            raise ValidationError('Invalid stream.')


class ListField(fields.List):
    def _validate(self, value):
        if isinstance(value, str):
            if not value:
                value = []
            else:
                value = value.split(',')

        return super()._validate(value)

    def _deserialize(self, value, attr=None, data=None, **kwargs):
        if isinstance(value, str):
            if not value:
                value = []
            else:
                value = value.split(',')
        return super()._deserialize(value, attr, data, **kwargs)


class RangeField(ListField):
    def _validate(self, value):
        super()._validate(value)
        if len(value) != 2:
            raise ValidationError('Must contain only 2 values')


class MultiRangeField(fields.Field):
    def _validate(self, value):
        if not isinstance(value, list):
            raise ValidationError('InvalidMultiRangeData')

        for r in value:
            if not isinstance(r, list):
                raise ValidationError('InvalidMultiRangeData')
            if len(r) != 2:
                raise ValidationError('InvalidMultiRangeData')
            for r_v in r:
                if not isinstance(r_v, (str, int, float)):
                    raise ValidationError('InvalidMultiRangeData')

    def _deserialize(self, value, attr=None, data=None, **kwargs):

        try:
            ranges = json.loads(value)
        except json.JSONDecodeError:
            raise ValidationError('InvalidMultiRangeData')

        return ranges


class TimeField(StringField):
    def _validate(self, value):
        super()._validate(value)
        if len(value) > 5:
            raise ValidationError('Invalid time.')
        try:
            hour, minute = value.split(':')
            hour = int(hour)
            minute = int(minute)
        except ValueError:
            raise ValidationError('Invalid time.')

        if hour < 0 or hour > 24 or minute < 0 or minute > 59:
            raise ValidationError('Invalid time.')
