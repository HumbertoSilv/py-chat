from py_chat.models.user import Friend


def test_create_friend_successfully(user, other_user):
    # act
    friend = Friend(user_id=user.id, friend_id=other_user.id)

    # assert
    assert friend.user_id == user.id
    assert friend.friend_id == other_user.id
