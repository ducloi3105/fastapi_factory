from sqlalchemy import (Integer, Float, ForeignKey, JSON, Table, Boolean, DateTime, Enum)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import JSONB

from src.common.constants import STRING_LENGTH, MESSAGE_STATES
from src.bases.model import BaseModel, Person, Column, String


class Message(BaseModel):
    sender = Column(JSONB)
    receiver = Column(JSONB)
    cc = Column(JSONB)
    bcc = Column(JSONB)
    reply_to = Column(JSONB)
    uid = Column(Integer, index=True)
    message_id_header = Column(
        String(STRING_LENGTH['LONG']), index=True
    )
    in_reply_to = Column(
        String(STRING_LENGTH['LONG']), index=True
    )
    subject = Column(
        String(STRING_LENGTH['LONG'])
    )

    received_at = Column(DateTime, index=True)  # sort by
    size = Column(Integer, index=True)  # len body

    read = Column(Boolean, index=True)
    starred = Column(Boolean, index=True)
    state = Column(Enum(*MESSAGE_STATES, name='state'), index=True)

    folder_id = Column(
        String(STRING_LENGTH['UUID4']),
        ForeignKey('folder.id'),
        nullable=False,
        index=True
    )
    old_folder_id = Column(
        String(STRING_LENGTH['UUID4']),
        nullable=True,
        index=True
    )
    account_id = Column(
        String(STRING_LENGTH['UUID4']),
        ForeignKey('account.id'),
        nullable=False,
        index=True
    )
    thread_id = Column(
        String(STRING_LENGTH['UUID4']),
        ForeignKey('thread.id'),
        nullable=False,
        index=True
    )

    folder = relationship(
        'Folder',
        backref=backref('messages',
                        cascade='all,delete')
    )

    account = relationship(
        'Account',
        backref=backref('messages',
                        cascade='all,delete')
    )

    thread = relationship(
        'Thread',
        backref=backref('messages',
                        cascade='all,delete')
    )
