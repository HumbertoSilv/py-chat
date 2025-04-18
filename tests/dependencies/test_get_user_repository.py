import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from py_chat.api.dependencies import get_user_repository
from py_chat.models.repositories.user import UserRepository


@pytest.mark.asyncio
async def test_decode_token_successfully(db_session: AsyncSession):
    # act
    repository = await get_user_repository(db_session)

    # assert
    assert isinstance(repository, UserRepository)
