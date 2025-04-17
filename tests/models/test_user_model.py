from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from py_chat.models.user import User


@pytest.mark.asyncio
async def test_create_user_successfully(db_session: AsyncSession):
    # act
    new_user = User(username='test', email='test@example.com')

    await new_user.save(db_session)

    # arrange
    result = await db_session.execute(
        select(User).where(User.username == 'test')
    )
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


@pytest.mark.asyncio
async def test_create_user_sqlalchemy_error(db_session: AsyncSession):
    # arrange
    with patch.object(
        db_session, 'commit', new_callable=AsyncMock
    ) as mock_commit:
        mock_commit.side_effect = SQLAlchemyError()

        new_user = User(username='test', email='test@example.com')

        with pytest.raises(SQLAlchemyError):
            # act
            await new_user.save(db_session)


@pytest.mark.asyncio
async def test_update_user_successfully(db_session: AsyncSession, user: User):
    # act
    await user.update(db_session, username='new_username', email='new_email')

    # arrange
    updated_user = await db_session.get(User, user.id)

    # assert
    assert updated_user.username == 'new_username'
    assert updated_user.email == 'new_email'


@pytest.mark.asyncio
async def test_update_user_sqlalchemy_error(
    db_session: AsyncSession, user: User
):
    # arrange
    with patch.object(
        db_session, 'commit', new_callable=AsyncMock
    ) as mock_commit:
        mock_commit.side_effect = SQLAlchemyError()

        with pytest.raises(SQLAlchemyError):
            # act
            await user.update(
                db_session, username='new_username', email='new_email'
            )


@pytest.mark.asyncio
async def test_refresh_user_successfully(db_session: AsyncSession):
    # act
    new_user = User(username='test', email='test@example.com')

    await new_user.save(db_session)
    await new_user.refresh(db_session)

    # assert
    assert new_user.id is not None


@pytest.mark.asyncio
async def test_refresh_user_sqlalchemy_error(
    db_session: AsyncSession, user: User
):
    # arrange
    with patch.object(
        db_session, 'refresh', new_callable=AsyncMock
    ) as mock_commit:
        mock_commit.side_effect = SQLAlchemyError()

        with pytest.raises(SQLAlchemyError):
            # act
            await user.refresh(db_session)
