from collections.abc import AsyncGenerator
from contextlib import contextmanager
from datetime import datetime

import factory
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from py_chat.core.database import get_async_session
from py_chat.core.security import create_access_token
from py_chat.main import app
from py_chat.models.user import Base, Chat, User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test_{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')


@pytest.fixture
def token(user):
    token = create_access_token({'sub': str(user.id)})

    return token


@pytest_asyncio.fixture
async def db_session(engine) -> AsyncGenerator[AsyncSession, None]:
    AsyncSessionFactory = async_sessionmaker(
        engine,
        autoflush=False,
        expire_on_commit=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionFactory() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope='session')
async def engine():
    with PostgresContainer('postgres:16-alpine', driver='asyncpg') as postgres:
        psql_url = postgres.get_connection_url()
        _engine = create_async_engine(psql_url, future=True)

        async with _engine.begin():
            yield _engine


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 1, 1)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at') and hasattr(target, 'updated_at'):
            target.created_at = time
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest_asyncio.fixture
async def user(db_session: AsyncSession) -> User:
    user = UserFactory()

    await user.save(db_session)
    await user.refresh(db_session)
    return user


@pytest_asyncio.fixture
async def other_user(db_session: AsyncSession) -> User:
    user = UserFactory()

    await user.save(db_session)
    await user.refresh(db_session)
    return user


@pytest_asyncio.fixture
async def chat(db_session: AsyncSession) -> Chat:
    chat = Chat(chat_type='direct')

    db_session.add(chat)
    await db_session.commit()
    await db_session.refresh(chat)

    return chat


@pytest_asyncio.fixture
async def client(
    db_session: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:
    # Session dependency override
    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_async_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
        yield client

    app.dependency_overrides.clear()
