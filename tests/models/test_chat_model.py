import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from py_chat.models.user import Chat, ChatParticipant


@pytest.mark.asyncio
async def test_should_create_a_direct_type_chat_successfully(
    db_session: AsyncSession,
):
    # act
    new_chat = Chat(chat_type='direct')

    db_session.add(new_chat)
    await db_session.commit()
    await db_session.refresh(new_chat)

    # arrange
    chat = await db_session.get(Chat, new_chat.id)

    # assert
    assert chat.chat_type == 'direct'


@pytest.mark.asyncio
async def test_should_create_a_group_type_chat_successfully(
    db_session: AsyncSession,
):
    # act
    new_chat = Chat(chat_type='group')

    db_session.add(new_chat)
    await db_session.commit()
    await db_session.refresh(new_chat)

    # arrange
    chat = await db_session.get(Chat, new_chat.id)

    # assert
    assert chat.chat_type == 'group'


@pytest.mark.asyncio
async def test_should_add_users_in_a_chat(
    db_session: AsyncSession, user, other_user, chat
):
    # act
    chat.users.append(user)
    chat.users.append(other_user)

    db_session.add(chat)
    await db_session.commit()
    await db_session.refresh(chat)

    # arrange
    NUMBER_OF_PARTICIPANTS_IN_CHAT = 2
    result = await db_session.execute(
        select(ChatParticipant).where(ChatParticipant.chat_id == chat.id)
    )

    chat_participants = result.scalars().all()

    # assert
    assert len(chat_participants) == NUMBER_OF_PARTICIPANTS_IN_CHAT
    for participant in chat_participants:
        assert isinstance(participant, ChatParticipant)
        assert participant.user_id in {user.id, other_user.id}
        assert participant.chat_id == chat.id
