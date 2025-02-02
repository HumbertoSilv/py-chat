import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(
        init=False, primary_key=True, default_factory=lambda: str(uuid.uuid4())
    )
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(init=False, nullable=True)
    avatar_url: Mapped[str] = mapped_column(init=False, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


@table_registry.mapped_as_dataclass
class Friend:
    __tablename__ = 'friends'

    user_id: Mapped[str] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), primary_key=True
    )
    friend_id: Mapped[str] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), primary_key=True
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
