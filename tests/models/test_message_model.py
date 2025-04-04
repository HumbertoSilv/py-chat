from sqlalchemy import select

from py_chat.models.user import Message


def test_should_create_a_TEXT_message_successfully(session, user, chat):
    # act
    new_message = Message(
        content='message test', user_id=user.id, chat_id=chat.id
    )

    session.add(new_message)
    session.commit()
    session.refresh(new_message)

    # arrange
    saved_message = session.scalar(
        select(Message).where(Message.id == new_message.id)
    )

    # assert
    assert saved_message.message_type == 'text'
    assert saved_message.content is not None
    assert saved_message.user_id == user.id
    assert saved_message.chat_id == chat.id


def test_should_create_a_FILE_message_successfully(session, user, chat):
    # act
    new_message = Message(
        content='message test',
        message_type='file',
        user_id=user.id,
        chat_id=chat.id,
    )

    session.add(new_message)
    session.commit()
    session.refresh(new_message)

    # arrange
    saved_message = session.scalar(
        select(Message).where(Message.id == new_message.id)
    )

    # assert
    assert saved_message.message_type == 'file'
    assert saved_message.content is not None
    assert saved_message.user_id == user.id
    assert saved_message.chat_id == chat.id
