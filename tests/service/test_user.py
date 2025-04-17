import pytest
from fastapi import HTTPException

from py_chat.models.repositories.user import UserRepository
from py_chat.models.user import User
from py_chat.schemas.user import CreateUserSchema
from py_chat.service.user import create_user, search_users_by_username


@pytest.mark.asyncio
async def test_service_to_create_users_successfully(
    user_repository: UserRepository,
):
    # arrange
    payload = CreateUserSchema(username='test', email='test@example.com')

    # act
    new_user = await create_user(user_repository, payload)

    # assert
    assert new_user.id is not None
    assert new_user.username == new_user.username
    assert new_user.email == new_user.email
    assert new_user.name is None
    assert new_user.avatar_url is None
    assert new_user.created_at == new_user.created_at
    assert new_user.updated_at == new_user.updated_at


@pytest.mark.asyncio
async def test_service_to_create_users_with_email_error(
    user_repository: UserRepository,
):
    # arrange
    payload_1 = CreateUserSchema(username='test_1', email='test_1@example.com')
    payload_2 = CreateUserSchema(username='test_2', email='test_1@example.com')

    await create_user(user_repository, payload_1)

    with pytest.raises(HTTPException):
        # act
        await create_user(user_repository, payload_2)


@pytest.mark.asyncio
async def test_service_to_create_users_with_username_error(
    user_repository: UserRepository,
):
    # arrange
    payload_1 = CreateUserSchema(username='test_1', email='test_1@example.com')
    payload_2 = CreateUserSchema(username='test_1', email='test_2@example.com')

    await create_user(user_repository, payload_1)

    with pytest.raises(HTTPException):
        # act
        await create_user(user_repository, payload_2)


@pytest.mark.asyncio
async def test_service_to_search_users_by_username_successfully(
    user_repository: UserRepository, user: User
):
    # act
    user_found = await search_users_by_username(user_repository, user.username)

    # assert
    for usr in user_found:
        assert isinstance(usr, User)
        assert usr.id == user.id
        assert usr.username == user.username
        assert usr.email == user.email


@pytest.mark.asyncio
async def test_service_to_search_users_by_username_return_empty_value(
    user_repository: UserRepository,
):
    # act
    user_found = await search_users_by_username(user_repository, '')

    # assert
    assert user_found == []
