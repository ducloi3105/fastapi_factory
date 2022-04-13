from src.bases.schema import (
    BaseSchema,
    BaseListingSchema,
    Query,
    STRING_LENGTH_VALIDATORS
)


class GetSchema(BaseListingSchema):
    search_text: str | None = Query(None, max_length=STRING_LENGTH_VALIDATORS['LONG'])
