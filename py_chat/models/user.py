import enum
import uuid
from datetime import datetime
from typing import List

from sqlalchemy import Enum, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class BaseModel:
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default_factory=uuid.uuid4,
        init=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


class ChatType(str, enum.Enum):
    DIRECT = 'direct'
    GROUP = 'group'


class MessageType(str, enum.Enum):
    TEXT = 'text'
    FILE = 'file'


@table_registry.mapped_as_dataclass
class User(BaseModel):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(init=False, nullable=True)
    avatar_url: Mapped[str] = mapped_column(init=False, nullable=True)

    chats: Mapped[List['Chat']] = relationship(
        init=False, secondary='chat_participants', back_populates='users'
    )
    messages: Mapped[List['Message']] = relationship(
        init=False, back_populates='user'
    )


@table_registry.mapped_as_dataclass
class Friend:
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
        init=False, server_default=func.now()
    )
    user: Mapped['User'] = relationship(
        'User', init=False, foreign_keys=[user_id], backref='friends'
    )
    friend: Mapped['User'] = relationship(
        'User', init=False, foreign_keys=[friend_id]
    )


@table_registry.mapped_as_dataclass
class Chat(BaseModel):
    __tablename__ = 'chats'

    chat_type: Mapped[ChatType] = mapped_column(Enum(ChatType))
    users: Mapped[List['User']] = relationship(
        init=False, secondary='chat_participants', back_populates='chats'
    )
    messages: Mapped[List['Message']] = relationship(
        init=False, back_populates='chat', cascade='all,delete'
    )


@table_registry.mapped_as_dataclass
class ChatParticipant:
    __tablename__ = 'chat_participants'

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True
    )
    chat_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('chats.id'), primary_key=True
    )


@table_registry.mapped_as_dataclass
class Message(BaseModel):
    __tablename__ = 'messages'

    content: Mapped[uuid.UUID] = mapped_column(String(5000))
    file_name: Mapped[str] = mapped_column(
        String(50), init=False, nullable=True
    )
    file_path: Mapped[str] = mapped_column(
        String(1000), init=False, nullable=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'))
    chat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('chats.id'))
    chat: Mapped['Chat'] = relationship(init=False, back_populates='messages')
    user: Mapped['User'] = relationship(init=False, back_populates='messages')
    message_type: Mapped[MessageType] = mapped_column(
        Enum(MessageType), default=MessageType.TEXT
    )
