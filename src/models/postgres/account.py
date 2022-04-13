from sqlalchemy import (ForeignKey, Table)
from src.common.constants import STRING_LENGTH
from src.bases.model import BaseModel, Person, Column, String


class Account(BaseModel):
    name = Column(String(STRING_LENGTH['SHORT']),
                  index=True)
    email = Column(String(STRING_LENGTH['SHORT']),
                   nullable=False, index=True)
