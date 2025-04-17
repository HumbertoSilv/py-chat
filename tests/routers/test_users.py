from http import HTTPStatus

import pytest

from py_chat.schemas.user import UserPublic

# test structure
# - Organizar(Arrange)
# - Agir(Act)
# - Afirmar(Assert)
# - Teardown


@pytest.mark.asyncio
async def test_create_user_successfully(client):
    # act
    response = await client.post(
        '/users/create',
        json={
            'username': 'test',
            'email': 'test@example.com',
        },
    )

    # assert
    assert response.status_code == HTTPStatus.CREATED
    assert isinstance(response.json().get('id'), str)


@pytest.mark.asyncio
async def test_should_return_already_existing_username_error(client, user):
    # act
    response = await client.post(
        '/users/create',
        json={'username': user.username, 'email': 'test@example.com'},
    )

    # assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


@pytest.mark.asyncio
async def test_should_return_already_existing_email_error(client, user):
    # act
    response = await client.post(
        '/users/create',
        json={
            'username': 'user',
            'email': user.email,
        },
    )

    # assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


@pytest.mark.asyncio
async def test_should_return_profile_data(client, token, user):
    # arrange
    user_schema = UserPublic.model_validate(user).model_dump()

    # act
    response = await client.get(
        '/users/profile', headers={'Authorization': f'Bearer {token}'}
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


@pytest.mark.asyncio
async def test_should_return_an_list_of_users(client, user):
    # arrange
    user_schema = UserPublic.model_validate(user).model_dump()

    # act
    response = await client.get(
        '/users/search',
        params={'username': user.username},
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [user_schema]


# TODO: cover up error scenarios
