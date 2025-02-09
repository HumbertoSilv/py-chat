import uuid
from http import HTTPStatus


def test_should_add_a_new_friend_successfully(client, user, other_user):
    # act
    response = client.post(
        f'/friends/{user.id}',
        json={
            'id': str(other_user.id),
        },
    )

    # assert
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_should_return_error_when_not_finding_user_id(client):
    # act
    invalid_user_Id = uuid.uuid4()
    response = client.post(
        f'/friends/{invalid_user_Id}',
        json={
            'id': str(invalid_user_Id),
        },
    )

    # assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_should_return_error_when_friendship_already_exists(
    client, user, other_user
):
    # arrange
    client.post(
        f'/friends/{user.id}',
        json={
            'id': str(other_user.id),
        },
    )

    # act
    response = client.post(
        f'/friends/{user.id}',
        json={
            'id': str(other_user.id),
        },
    )

    # assert
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Friendship already exists'}


def test_should_return_a_users_friendships_successfully(
    client, user, other_user
):
    # arrange
    client.post(
        f'/friends/{user.id}',
        json={
            'id': str(other_user.id),
        },
    )

    # act
    response = client.get(f'/friends/{user.id}')

    # assert
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json()['friends'], list)
    assert len(response.json()['friends']) == 1
    assert response.json()['friends'][0].get('username') == other_user.username
