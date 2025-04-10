import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from py_chat.models.user import User


@pytest.mark.asyncio
async def test_create_user_successfully(session: AsyncSession):
    # act
    new_user = User(username='test', email='test@example.com')

    session.add(new_user)
    await session.commit()

    # arrange
    result = await session.execute(select(User).where(User.username == 'test'))
    user = result.scalars().first()

    # assert
    assert user.id is not None
    assert user.username == new_user.username
    assert user.email == new_user.email
    assert user.name is None
    assert user.avatar_url is None
    assert user.chats == []
    assert user.messages == []
    assert user.created_at == new_user.created_at
    assert user.updated_at == new_user.updated_at
