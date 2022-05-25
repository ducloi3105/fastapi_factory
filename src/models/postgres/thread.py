from sqlalchemy import (Table, Integer, Float, ForeignKey, JSON, Boolean, String, DateTime, Index, text)
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import relationship, backref

from src.common.constants import STRING_LENGTH
from src.bases.model import BaseModel, Person, Column, String


class Thread(BaseModel):
    account_id = Column(
        String(STRING_LENGTH['UUID4']),
        ForeignKey('account.id'),
        nullable=False,
        index=True
    )
    read = Column(Boolean, default=False)
    starred = Column(Boolean, default=False)
    has_attachments = Column(Boolean)
    subject = Column(String(STRING_LENGTH['MEDIUM']), index=True)

    last_message_at = Column(DateTime, index=True)
    participants = Column(JSONB, index=True)

    folders = Column(ARRAY(String), index=True)
    snippets = Column(JSONB, index=True)

    account = relationship(
        'Account',
        backref=backref('threads',
                        cascade='all,delete')
    )

    __table_args__ = (
        Index('ix_thread_folders', folders, postgresql_using="gin"),
    )
