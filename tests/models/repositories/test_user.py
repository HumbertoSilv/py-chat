from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from py_chat.models.repositories.user import UserRepository
from py_chat.models.user import User
from py_chat.schemas.user import UserUpdateSchema


@pytest.mark.asyncio
async def test_create_user_successfully(db_session: AsyncSession):
    # act
    user_repository = UserRepository(db_session)
    new_user = await user_repository.create_user(
        username='test', email='test@example.com'
    )

    # arrange
    result = await db_session.execute(
        select(User).where(User.id == new_user.id)
    )
    created_user = result.scalars().first()

    # assert
    assert created_user.username == new_user.username
    assert created_user.email == new_user.email
    assert created_user.name is None
    assert created_user.avatar_url is None
    assert created_user.chats == []
    assert created_user.messages == []
    assert created_user.created_at == new_user.created_at
    assert created_user.updated_at == new_user.updated_at


@pytest.mark.asyncio
async def test_create_user_sqlalchemy_error(db_session: AsyncSession):
    # arrange
    with patch.object(
        db_session, 'commit', new_callable=AsyncMock
    ) as mock_commit:
        mock_commit.side_effect = SQLAlchemyError()
        user_repository = UserRepository(db_session)

        with pytest.raises(SQLAlchemyError):
            # act
            await user_repository.create_user(
                username='test', email='test@example.com'
            )


@pytest.mark.asyncio
async def test_get_user_successfully(db_session: AsyncSession, user: User):
    # act
    user_repository = UserRepository(db_session)
    user_result = await user_repository.get_user_by_ID(user.id)

    # assert
    assert user_result.id == user.id
    assert user_result.username == user.username
    assert user_result.email == user.email


@pytest.mark.asyncio
async def test_get_user_sqlalchemy_error(db_session: AsyncSession, user: User):
    # arrange
    with patch.object(
        db_session, 'get', new_callable=AsyncMock
    ) as mock_commit:
        mock_commit.side_effect = SQLAlchemyError()
        user_repository = UserRepository(db_session)

        with pytest.raises(SQLAlchemyError):
            # act
            await user_repository.get_user_by_ID(user.id)


@pytest.mark.asyncio
async def test_get_user_by_email_successfully(
    db_session: AsyncSession, user: User
):
    # act
    user_repository = UserRepository(db_session)
    user_result = await user_repository.get_user_by_email(user.email)

    # assert
    assert user_result.id == user.id
    assert user_result.username == user.username
    assert user_result.email == user.email


@pytest.mark.asyncio
async def test_get_user_by_email_sqlalchemy_error(
    db_session: AsyncSession, user: User
):
    # arrange
    with patch.object(
        db_session, 'execute', new_callable=AsyncMock
    ) as mock_commit:
        mock_commit.side_effect = SQLAlchemyError()
        user_repository = UserRepository(db_session)

        with pytest.raises(SQLAlchemyError):
            # act
            await user_repository.get_user_by_email(user.email)


@pytest.mark.asyncio
async def test_get_user_by_username_successfully(
    db_session: AsyncSession, user: User
):
    # act
    user_repository = UserRepository(db_session)
    user_result = await user_repository.get_user_by_username(user.username)

    # assert
    assert user_result.id == user.id
    assert user_result.username == user.username
    assert user_result.email == user.email


@pytest.mark.asyncio
async def test_get_user_by_username_sqlalchemy_error(
    db_session: AsyncSession, user: User
):
    # arrange
    with patch.object(
        db_session, 'execute', new_callable=AsyncMock
    ) as mock_commit:
        mock_commit.side_effect = SQLAlchemyError()
        user_repository = UserRepository(db_session)

        with pytest.raises(SQLAlchemyError):
            # act
            await user_repository.get_user_by_username(user.username)


@pytest.mark.asyncio
async def test_update_user_successfully(db_session: AsyncSession, user: User):
    update_payload = UserUpdateSchema(
        name='new_name', avatar_url='new_avatar_url'
    )
    # act
    user_repository = UserRepository(db_session)
    await user_repository.update_user(user.id, update_payload)

    # arrange
    result = await db_session.execute(select(User).where(User.id == user.id))
    updated_user = result.scalars().first()

    # assert
    assert updated_user.name == 'new_name'
    assert updated_user.avatar_url == 'new_avatar_url'


@pytest.mark.asyncio
async def test_update_user_sqlalchemy_error(
    db_session: AsyncSession, user: User
):
    update_payload = UserUpdateSchema(
        name='new_name', avatar_url='new_avatar_url'
    )
    # arrange
    with patch.object(
        db_session, 'commit', new_callable=AsyncMock
    ) as mock_commit:
        mock_commit.side_effect = SQLAlchemyError()
        user_repository = UserRepository(db_session)

        with pytest.raises(SQLAlchemyError):
            # act
            await user_repository.update_user(user.id, update_payload)
