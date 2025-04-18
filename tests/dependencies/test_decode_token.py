from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest
from freezegun import freeze_time

from py_chat.api.dependencies import decode_token
from py_chat.core.config import Settings
from py_chat.models.user import User

settings = Settings()


@pytest.mark.asyncio
async def test_decode_token_successfully(token, user: User):
    # act
    decoded_token = decode_token(token)

    # assert
    assert decoded_token.get('sub') == str(user.id)


@pytest.mark.asyncio
async def test_should_simulate_a_DecodeError(token):
    # arrange
    invalid_token = token[:-1]

    # act
    decoded_token = decode_token(invalid_token)

    # assert
    assert decoded_token is None


@pytest.mark.asyncio
async def test_should_simulate_a_ExpiredSignatureError(token):
    # arrange
    future_time = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES
    )

    with freeze_time(future_time):
        # act
        decoded_token = decode_token(token)

    # assert
    assert decoded_token is None
