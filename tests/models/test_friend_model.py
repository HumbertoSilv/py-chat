import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from py_chat.models.user import Friend


@pytest.mark.asyncio
async def test_create_friend_successfully(
    db_session: AsyncSession, user, other_user
):
    # act
    new_friend = Friend(user_id=user.id, friend_id=other_user.id)
    db_session.add(new_friend)
    await db_session.commit()

    # arrange
    result = await db_session.execute(
        select(Friend).where(
            Friend.user_id == user.id, Friend.friend_id == other_user.id
        )
    )
    friend = result.scalars().first()

    # assert
    assert friend is not None
    assert friend.user_id == user.id
    assert friend.friend_id == other_user.id
