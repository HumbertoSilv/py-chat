import uuid
from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_should_add_a_new_friend_successfully(client, token, other_user):
    # act
    response = await client.post(
        '/friends/add',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'id': str(other_user.id),
        },
    )

    # assert
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_should_return_error_when_not_finding_user_id(client, token):
    # act
    invalid_user_Id = uuid.uuid4()
    response = await client.post(
        '/friends/add',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'id': str(invalid_user_Id),
        },
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


@pytest.mark.asyncio
async def test_should_return_error_when_friendship_already_exists(
    client, token, other_user
):
    # arrange
    await client.post(
        '/friends/add',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'id': str(other_user.id),
        },
    )

    # act
    response = await client.post(
        '/friends/add',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'id': str(other_user.id),
        },
    )

    # assert
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Friendship already exists'}


@pytest.mark.asyncio
async def test_should_return_a_users_friendships_successfully(
    client, token, other_user
):
    # arrange
    await client.post(
        '/friends/add',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'id': str(other_user.id),
        },
    )

    # act
    response = await client.get(
        '/friends/list', headers={'Authorization': f'Bearer {token}'}
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json()['friends'], list)
    assert len(response.json()['friends']) == 1
    assert response.json()['friends'][0].get('username') == other_user.username
