from sqlalchemy import (Table, Integer, Float, ForeignKey, JSON, Boolean, String, DateTime)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, backref

from src.common.constants import STRING_LENGTH
from src.bases.model import BaseModel, Person, Column, String


class Setting(BaseModel):
    account_id = Column(
        String(STRING_LENGTH['UUID4']),
        ForeignKey('account.id'),
        index=True
    )

    key = Column(String(STRING_LENGTH['MEDIUM']), nullable=False)
    value = Column(String(STRING_LENGTH['MEDIUM']), nullable=False)

    account = relationship(
        'Account',
        backref=backref('settings',
                        cascade='all,delete')
    )
