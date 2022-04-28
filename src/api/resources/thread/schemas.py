from src.bases.schema import BaseListingSchema


class GetSchema(BaseListingSchema):
    search_text: str
    folder: str
