import uuid
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)

from py_chat.core.logger import logger


class Base(DeclarativeBase):
    async def save(self, db_session: AsyncSession):
        """Save the instance to the database."""

        try:
            db_session.add(self)
            await db_session.commit()

        except SQLAlchemyError as exception:
            logger.debug(
                f'Error inserting instance of {self}: {repr(exception)}'
            )
            await db_session.rollback()
            raise exception

    async def update(self, db_session: AsyncSession, **kwargs):
        """Update the instance to the database."""
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            await db_session.commit()

        except SQLAlchemyError as exception:
            logger.debug(
                f'Error updating instance of {self}: {repr(exception)}'
            )
            await db_session.rollback()
            raise exception

    async def refresh(self, db_session: AsyncSession):
        """refresh the instance to the database."""

        try:
            await db_session.refresh(self)

        except SQLAlchemyError as exception:
            logger.debug(
                f'Error refreshing instance of {self}: {repr(exception)}'
            )
            raise exception


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
