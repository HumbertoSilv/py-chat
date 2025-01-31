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
        }
    )

    # assert
    assert response.status_code == HTTPStatus.CREATED
    assert isinstance(response.json()['id'], str)
