from contextlib import contextmanager
from datetime import datetime

import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine, event
from sqlalchemy.orm import Session

from py_chat.core.database import get_session
from py_chat.main import app
from py_chat.models.user import User, table_registry


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test_{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')


@pytest.fixture
def session():
    # sqlite in memorie
    engine = create_engine(
        'sqlite://',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


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


@pytest.fixture
def client(session):
    def get_client_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_client_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user(session):
    user = UserFactory()

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def other_user(session):
    user = UserFactory()

    session.add(user)
    session.commit()
    session.refresh(user)

    return user
