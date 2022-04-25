from sqlalchemy import (Table, Integer, Float, ForeignKey, JSON, Boolean, String, DateTime)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, backref

from src.common.constants import STRING_LENGTH
from src.bases.model import BaseModel, Person, Column, String


class Participant(BaseModel):
    email = Column(String(STRING_LENGTH['MEDIUM']), nullable=False, index=True)
    name = Column(String(STRING_LENGTH['MEDIUM']), nullable=False, index=True)

    account_id = Column(
        String(STRING_LENGTH['UUID4']),
        ForeignKey('account.id'),
        nullable=False,
        index=True
    )

    account = relationship(
        'Account',
        backref=backref('participants',
                        cascade='all,delete')
    )
