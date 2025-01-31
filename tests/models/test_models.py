from dataclasses import asdict

from sqlalchemy import select

from py_chat.models.user import User


def test_create_user_successfully(session, mock_db_time):
    # act
    with mock_db_time(model=User) as time:
        new_user = User(username='test', email='test@example.com')

        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == 'test'))

    # assert
    assert asdict(user) == {
        'id': user.id,
        'username': 'test',
        'email': 'test@example.com',
        'name': None,
        'avatar_url': None,
        'created_at': time,
        'updated_at': time,
    }
