import enum
import uuid
from datetime import datetime
from typing import List

from sqlalchemy import Enum as SQLAEnum
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from py_chat.models.base import Base, BaseModel


class ChatType(str, enum.Enum):
    DIRECT = 'direct'
    GROUP = 'group'


class MessageType(str, enum.Enum):
    TEXT = 'text'
    FILE = 'file'


class User(BaseModel):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(200), nullable=True)

    chats: Mapped[List['Chat']] = relationship(
        secondary='chat_participants',
        back_populates='users',
        lazy='selectin',
    )
    messages: Mapped[List['Message']] = relationship(
        back_populates='user', lazy='selectin'
    )


class Friend(Base):
    __tablename__ = 'friends'

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True,
    )
    friend_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )

    user: Mapped['User'] = relationship(
        foreign_keys=[user_id],
        backref='friends',
        lazy='selectin',
    )
    friend: Mapped['User'] = relationship(
        foreign_keys=[friend_id],
        lazy='selectin',
    )


class Chat(BaseModel):
    __tablename__ = 'chats'

    chat_type: Mapped[ChatType] = mapped_column(SQLAEnum(ChatType))
    users: Mapped[List['User']] = relationship(
        secondary='chat_participants',
        back_populates='chats',
        lazy='selectin',
    )
    messages: Mapped[List['Message']] = relationship(
        back_populates='chat',
        cascade='all,delete',
        lazy='selectin',
    )


class ChatParticipant(Base):
    __tablename__ = 'chat_participants'

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True
    )
    chat_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('chats.id'), primary_key=True
    )


class Message(BaseModel):
    __tablename__ = 'messages'

    content: Mapped[str] = mapped_column(String(5000))
    file_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    file_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'))
    chat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('chats.id'))

    user: Mapped['User'] = relationship(
        back_populates='messages', lazy='selectin'
    )
    chat: Mapped['Chat'] = relationship(
        back_populates='messages', lazy='selectin'
    )

    message_type: Mapped[MessageType] = mapped_column(
        SQLAEnum(MessageType), default=MessageType.TEXT
    )
