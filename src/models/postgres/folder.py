from sqlalchemy import (Integer, Float, ForeignKey, JSON, Table, Boolean)
from sqlalchemy.orm import relationship, backref

from src.common.constants import STRING_LENGTH
from src.bases.model import BaseModel, Person, Column, String


class Folder(BaseModel):
    account_id = Column(String(STRING_LENGTH['UUID4']),
                        nullable=False, index=True)

    name = Column(String(STRING_LENGTH['SHORT']),
                  nullable=False, index=True)

    display_name = Column(String(STRING_LENGTH['SHORT']),
                          nullable=False, index=True)

    color = Column(String(STRING_LENGTH['SHORT']), index=True)

    account = relationship('Account',
                           backref=backref('folders',
                                           cascade='all,delete'))
