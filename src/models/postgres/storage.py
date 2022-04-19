from sqlalchemy import (Table, Integer, Float, ForeignKey, JSON, Boolean, String, DateTime)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, backref

from src.common.constants import STRING_LENGTH
from src.bases.model import BaseModel, Person, Column, String


class Storage(BaseModel):
    filename = Column(String(STRING_LENGTH['LONG']), index=True, nullable=False)
    filetype = Column(String(STRING_LENGTH['LONG']), index=True)
    content_type = Column(String(STRING_LENGTH['LONG']), index=True,
                          nullable=False)
    size = Column(Integer, default=0)

    object_type = Column(String(STRING_LENGTH['LONG']), index=True)
    object_id = Column(String(STRING_LENGTH['UUID4']), index=True)

    url = Column(String(STRING_LENGTH['LARGE']), index=True, nullable=False)

    has_virus = Column(Boolean, index=True, default=False)

    meta = Column(JSONB)

    account_id = Column(
        String(STRING_LENGTH['UUID4']),
        ForeignKey('account.id'),
        nullable=False,
        index=True
    )

    account = relationship(
        'Account',
        backref=backref('files',
                        cascade='all,delete')
    )
