from sqlalchemy import (Table, Integer, Float, ForeignKey, JSON, Boolean, String, DateTime)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, backref

from src.common.constants import STRING_LENGTH
from src.bases.model import BaseModel, Person, Column, String


class Tracker(BaseModel):
    """Model representing a tracker image."""
    message_id = Column(
        String(STRING_LENGTH['UUID4']),
        ForeignKey('message.id'),
        index=True
    )
    thread_id = Column(
        String(STRING_LENGTH['UUID4']),
        ForeignKey('thread.id'),
        index=True
    )
    sender = Column(String(STRING_LENGTH['LONG']))
    view_count = Column(Integer, default=0, index=True)
    is_muted = Column(Boolean, default=False, index=True)
    first_seen = Column(DateTime, index=True)
    last_seen = Column(DateTime, index=True)

    message = relationship(
        'Message',
        backref=backref('message',
                        cascade='all,delete',
                        uselist=False)
    )
    thread = relationship(
        'Thread',
        backref=backref('thread',
                        cascade='all,delete',
                        uselist=False)
    )
