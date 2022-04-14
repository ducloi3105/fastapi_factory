from sqlalchemy import (Table, Integer, Float, ForeignKey, JSON, Boolean, String, DateTime)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, backref

from src.common.constants import STRING_LENGTH
from src.bases.model import BaseModel, Person, Column, String


class Verification(BaseModel):
    account_id = Column(
        String(STRING_LENGTH['UUID4']),
        ForeignKey('account.id'),
        index=True
    )

    receiver = Column(String(STRING_LENGTH['LONG']), index=True)
    code = Column(String(STRING_LENGTH['SHORT']), index=True)
    type = Column(String(STRING_LENGTH['SHORT']), index=True)
    verified_at = Column(DateTime, index=True)
    verified = Column(Boolean, default=False, index=True)
    expire_at = Column(DateTime, index=True)

    account = relationship(
        'Account',
        backref=backref('verifications',
                        cascade='all,delete')
    )
