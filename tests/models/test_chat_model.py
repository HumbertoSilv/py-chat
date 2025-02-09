from sqlalchemy import select

from py_chat.models.user import Chat, ChatParticipant


def test_should_create_a_direct_type_chat_successfully(session):
    # act
    new_chat = Chat(chat_type='direct')

    session.add(new_chat)
    session.commit()
    session.refresh(new_chat)

    # arrange
    chat = session.scalar(select(Chat).where(Chat.id == new_chat.id))

    # assert
    assert chat.chat_type == 'direct'


def test_should_create_a_group_type_chat_successfully(session):
    # act
    new_chat = Chat(chat_type='group')

    session.add(new_chat)
    session.commit()
    session.refresh(new_chat)

    # arrange
    chat = session.scalar(select(Chat).where(Chat.id == new_chat.id))

    # assert
    assert chat.chat_type == 'group'


def test_should_add_users_in_a_chat(session, user, other_user, chat):
    # act
    chat.users.append(user)
    chat.users.append(other_user)

    session.add(chat)
    session.commit()
    session.refresh(chat)

    # arrange
    NUMBER_OF_PARTICIPANTS_IN_CHAT = 2
    chat_participants = session.scalars(
        select(ChatParticipant).where(ChatParticipant.chat_id == chat.id)
    ).all()

    # assert
    assert len(chat_participants) == NUMBER_OF_PARTICIPANTS_IN_CHAT
    for participant in chat_participants:
        assert isinstance(participant, ChatParticipant)
        assert participant.user_id in {user.id, other_user.id}
        assert participant.chat_id == chat.id
