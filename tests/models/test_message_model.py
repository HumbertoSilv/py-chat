import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from py_chat.models.user import Message


@pytest.mark.asyncio
async def test_should_create_a_TEXT_message_successfully(
    db_session: AsyncSession, user, chat
):
    # act
    new_message = Message(
        content='message test', user_id=user.id, chat_id=chat.id
    )

    db_session.add(new_message)
    await db_session.commit()
    await db_session.refresh(new_message)

    # arrange
    saved_message = await db_session.get(Message, new_message.id)

    # assert
    assert saved_message.content == 'message test'
    assert saved_message.message_type == 'text'
    assert saved_message.user_id == user.id
    assert saved_message.chat_id == chat.id


@pytest.mark.asyncio
async def test_should_create_a_FILE_message_successfully(
    db_session, user, chat
):
    # act
    new_message = Message(
        content='file_url',
        message_type='file',
        user_id=user.id,
        chat_id=chat.id,
    )

    db_session.add(new_message)
    await db_session.commit()
    await db_session.refresh(new_message)

    # arrange
    saved_message = await db_session.get(Message, new_message.id)

    # assert
    assert saved_message.content == 'file_url'
    assert saved_message.message_type == 'file'
    assert saved_message.user_id == user.id
    assert saved_message.chat_id == chat.id
