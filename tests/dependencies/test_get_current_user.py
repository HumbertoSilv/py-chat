from datetime import datetime, timedelta
from http import HTTPStatus
from uuid import uuid4
from zoneinfo import ZoneInfo

import pytest
from fastapi import HTTPException
from freezegun import freeze_time
from jwt import encode
from sqlalchemy.ext.asyncio import AsyncSession

from py_chat.api.dependencies import get_current_user
from py_chat.core.config import Settings
from py_chat.models.user import User

settings = Settings()


@pytest.mark.asyncio
async def test_should_return_the_current_user_successfully(
    db_session: AsyncSession, token: str
):
    # act
    user = await get_current_user(db_session, token)

    # assert
    assert isinstance(user, User)


@pytest.mark.asyncio
async def test_without_sub_in_payload_should_return_error(
    db_session: AsyncSession,
):
    # arrange
    token = encode(
        {},
        settings.SECRET_KEY,
        settings.ALGORITHM,
    )

    with pytest.raises(HTTPException) as exc_info:
        # act
        await get_current_user(db_session, token)

    # assert
    assert exc_info.value.detail == 'Could not validate credentials'
    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_should_return_a_DecodeError(db_session: AsyncSession):
    # arrange
    token = encode(
        {},
        'TEST_INVALID_SECRET_KEY',
        settings.ALGORITHM,
    )

    with pytest.raises(HTTPException) as exc_info:
        # act
        await get_current_user(db_session, token)

    # assert
    assert exc_info.value.detail == 'Could not validate credentials'
    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_should_return_a_ExpiredSignatureError(db_session: AsyncSession):
    with freeze_time('2023-12-11 12:00:00'):
        # arrange
        expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES
        )
        token = encode(
            {'sub': 'fake_sub', 'exp': expire},
            settings.SECRET_KEY,
            settings.ALGORITHM,
        )

    with freeze_time('2023-12-11 12:31:00'):
        with pytest.raises(HTTPException) as exc_info:
            # act
            await get_current_user(db_session, token)

        # assert
        assert exc_info.value.detail == 'Signature has expired'
        assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_should_return_an_error_if_it_does_not_find_a_user(
    db_session: AsyncSession,
):
    # arrange
    token = encode(
        {'sub': str(uuid4())},
        settings.SECRET_KEY,
        settings.ALGORITHM,
    )

    with pytest.raises(HTTPException) as exc_info:
        # act
        await get_current_user(db_session, token)

    # assert
    assert exc_info.value.detail == 'Could not validate credentials'
    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED
