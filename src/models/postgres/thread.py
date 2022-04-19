from sqlalchemy import (Table, Integer, Float, ForeignKey, JSON, Boolean, String, DateTime)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, backref

from src.common.constants import STRING_LENGTH
from src.bases.model import BaseModel, Person, Column, String

folders = Table(
    'thread_folder_association',
    BaseModel.metadata,
    Column(
        'thread_id',
        String(STRING_LENGTH['UUID4']),
        ForeignKey('thread.id', ondelete='CASCADE'),
        primary_key=True
    ),
    Column(
        'folder_id',
        String(STRING_LENGTH['UUID4']),
        ForeignKey('folder.id', ondelete='CASCADE'),
        primary_key=True
    )
)


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
    snippet = Column(String(STRING_LENGTH['MEDIUM']))
    snippets = Column(JSONB)
    subject = Column(String(STRING_LENGTH['MEDIUM']), index=True)
    participants = Column(JSONB)

    last_message_at = Column(DateTime, index=True)

    # This column won't store any data, but is filled by custom query
    # See ThreadList for example.
    folders = relationship(
        'Folder',
        secondary=folders,
        backref=backref('threads')
    )

    account = relationship(
        'Account',
        backref=backref('threads',
                        cascade='all,delete')
    )
