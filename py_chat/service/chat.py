from sqlalchemy import and_, select
from sqlalchemy.orm import Session, subqueryload

from py_chat.models.user import Chat, ChatParticipant, User, ChatType


def create_direct_chat(
    db_session: Session,
    destination_user: User,
    initiator_user: User
) -> Chat:
    try:
        new_chat = Chat(chat_type=ChatType.DIRECT)
        new_chat.users.append(initiator_user)
        new_chat.users.append(destination_user)

        db_session.add(new_chat)
        db_session.commit()

        return new_chat

    except Exception as error:
        db_session.rollback()
        raise error


def get_user_chats(db_session: Session, user: str) -> list[Chat]:
    query = (
        select(Chat)
        .distinct()
        .join(ChatParticipant, ChatParticipant.chat_id == Chat.id)
        .where(ChatParticipant.user_id == user)
        .options(
            subqueryload(Chat.users),
            subqueryload(Chat.messages)
        )
    )

    chats = db_session.scalars(query).all()

    return chats
