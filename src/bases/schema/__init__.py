from pydantic import BaseModel
from fastapi import Query
from src.common.constants import PAGINATION, STRING_LENGTH


STRING_LENGTH_VALIDATORS = {
    'EX_SHORT': lambda value: len(value) <= STRING_LENGTH['EX_SHORT'],
    'SHORT': lambda value: len(value) <= STRING_LENGTH['SHORT'],
    'MEDIUM': lambda value: len(value) <= STRING_LENGTH['MEDIUM'],
    'LONG': lambda value: len(value) <= STRING_LENGTH['LONG'],
    'EX_LONG': lambda value: len(value) <= STRING_LENGTH['EX_LONG'],
    'LARGE': lambda value: len(value) <= STRING_LENGTH['LARGE'],
    'EX_LARGE': lambda value: len(value) <= STRING_LENGTH['EX_LARGE']
}


class BaseSchema(BaseModel):
    pass


class BaseListingSchema(BaseSchema):
    page: int | None = PAGINATION['page']
    per_page: int | None = PAGINATION['per_page']
    sorts: list | None = ['-created_at']
