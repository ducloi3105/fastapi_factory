from src.bases.schema import (
    BaseSchema,
    BaseListingSchema,
    Query,
    STRING_LENGTH_VALIDATORS
)


class GetSchema(BaseSchema):
    email: str


class PostSchema(BaseSchema):
    email: str 
    name: str | None = None