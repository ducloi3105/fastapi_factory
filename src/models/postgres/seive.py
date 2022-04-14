from sqlalchemy import (Table, Integer, Float, ForeignKey, JSON, Boolean, String, DateTime)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, backref

from src.common.constants import STRING_LENGTH
from src.bases.model import BaseModel, Person, Column, String


class Sieve(BaseModel):
    account_id = Column(
        String(STRING_LENGTH['UUID4']),
        ForeignKey('account.id'),
        index=True
    )

    name = Column(String(STRING_LENGTH['LONG']), index=True)
    sieve_script = Column(String(STRING_LENGTH['EX_LONG']), nullable=False)
    sieve_json = Column(JSONB, nullable=False)
    enable = Column(Boolean, default=False, index=True)

    account = relationship(
        'Account',
        backref=backref('sieves',
                        cascade='all,delete')
    )
