from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import subqueryload

from py_chat.models.user import Chat, ChatParticipant, ChatType, Message, User


async def create_direct_chat(
    session: AsyncSession, destination_user: User, initiator_user: User
) -> Chat:
    try:
        new_chat = Chat(chat_type=ChatType.DIRECT)
        new_chat.users.append(initiator_user)
        new_chat.users.append(destination_user)

        session.add(new_chat)
        await session.commit()

        return new_chat

    except Exception as error:
        session.rollback()
        raise error


async def get_user_chats(session: AsyncSession, user: UUID) -> list[Chat]:
    stmt = (
        select(Chat)
        # .distinct()
        .join(ChatParticipant, ChatParticipant.chat_id == Chat.id)
        .where(ChatParticipant.user_id == user)
        .options(
            subqueryload(Chat.users),
            subqueryload(Chat.messages),
        )
    )

    result = await session.execute(stmt)
    chats = result.scalars().all()

    return chats


async def get_latest_chat_message(
    session: AsyncSession, chat_id: UUID
) -> Message | None:
    stmt = (
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(Message.created_at.desc())
        .limit(1)
    )

    result = await session.execute(stmt)
    latest_message = result.scalars().first()

    return latest_message
