from http import HTTPStatus

# test structure
# - Organizar(Arrange)
# - Agir(Act)
# - Afirmar(Assert)
# - Teardown


def test_create_user_successfully(client):
    # act
    response = client.post(
        '/users',
        json={
            'username': 'test',
            'email': 'test@example.com',
        },
    )

    # assert
    assert response.status_code == HTTPStatus.CREATED
    assert isinstance(response.json().get('id'), str)


def test_should_return_already_existing_username_error(client, user):
    # act
    response = client.post(
        '/users',
        json={
            'username': user.username,
            'email': 'test@example.com'
        },
    )

    # assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_should_return_already_existing_email_error(client, user):
    # act
    response = client.post(
        '/users',
        json={
            'username': 'user',
            'email': user.email,
        },
    )

    # assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}
