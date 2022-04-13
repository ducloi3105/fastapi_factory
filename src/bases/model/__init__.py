import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, String, TIMESTAMP, Boolean, desc
from sqlalchemy.orm import Query as Query_

from src.common.constants import STRING_LENGTH, ISO_FORMAT
from src.common.utils import get_now
from src.common import dict_utils

Base = declarative_base()


class Query(Query_):
    def paginate(self, page: int = None, per_page: int = None):
        if not page:
            page = 1
        if not per_page:
            per_page = 20
        return self.offset((page - 1) * per_page).limit(per_page)

    def sort(self, table, *args):
        if not args:
            args = ['-created_at']

        sort_list = []
        for string in args:
            # get key, value of sort item
            try:
                key, value = string.split('==')
            except ValueError:
                key = string
                value = None

            # get column name and descending
            if key.startswith('-'):
                field_name = key[1:len(key)]
                descending = True
            else:
                descending = False
                if string.startswith('+'):
                    field_name = key[1:len(key)]
                else:
                    field_name = key

            # get sqlalchemy sort object
            field = getattr(table, field_name, None)
            if field:
                if value:
                    sort = field == value
                else:
                    sort = field

                if descending:
                    sort = desc(sort)
                sort_list.append(sort)

        if sort_list:
            return self.order_by(*sort_list)

        return self


class BaseModel(Base):
    __abstract__ = True

    query_class = Query

    @declared_attr
    def __tablename__(self):
        return ''.join('_%s' % c if c.isupper() else c
                       for c in self.__name__).strip('_').lower()

    id = Column(String(STRING_LENGTH['UUID4']),
                primary_key=True,
                default=lambda: str(uuid.uuid4()))

    created_at = Column(TIMESTAMP(timezone=True),
                        default=get_now,
                        index=True)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=get_now,
                        onupdate=get_now,
                        index=True)

    deleted = Column(Boolean, default=False, index=True)

    @classmethod
    def from_dict(cls, data, origin=None):
        if origin:
            if not isinstance(origin, cls):
                raise Exception('Invalid origin object of %s.' % cls.__name__)
            result = origin
        else:
            result = cls()

        result = result.update(**data)

        return result

    def _parse_value(self, value, **kwargs):
        if value is None:
            return None

        if isinstance(value, datetime):
            return value.isoformat()

        return value

    def to_json(self,
                include_fields=None,
                exclude_fields=None,
                **kwargs):
        result = dict()

        all_columns = self.__table__.columns
        for field in all_columns:
            value = getattr(self, field.name, None)
            value = self._parse_value(value)
            result[field.name] = value

        result = dict_utils.filter_keys(
            data=result,
            include_keys=include_fields,
            exclude_keys=exclude_fields,
            absolute=False
        )

        return result

    def update(self, **kwargs):

        columns = self.__table__.columns

        for field_name, value in kwargs.items():
            if field_name == 'id':
                continue

            col = columns.get(field_name, None)
            if col is None:
                continue

            setattr(self, field_name, value)
        return self

    def clone(self, excludes=None):
        _excludes = ['id', 'created_at', 'updated_at'] + (excludes or [])

        result = self.__class__()
        fields = self.__table__.columns
        for field_name in fields.keys():
            if field_name in _excludes:
                continue

            value = getattr(self, field_name, None)
            if value is None:
                continue

            setattr(result, field_name, value)
        return result


class Person(object):
    email = Column(String(STRING_LENGTH['LONG']), index=True)
    phone = Column(String(STRING_LENGTH['EX_SHORT']), index=True)
    name = Column(String(STRING_LENGTH['LONG']), index=True)
    address = Column(String(STRING_LENGTH['LONG']))
    gender = Column(String(STRING_LENGTH['EX_SHORT']), index=True)


class Translation(object):
    language_code = Column(String(STRING_LENGTH['LONG']),
                           index=True, nullable=False)
    name = Column(String(STRING_LENGTH['LONG']), index=True)
