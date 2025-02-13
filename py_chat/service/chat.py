from sqlalchemy.orm import Session

from py_chat.models.user import Chat, User, ChaType


def create_direct_chat(
    db_session: Session,
    destination_user: User,
    initiator_user: User
) -> Chat:
    try:
        new_chat = Chat(chat_type=ChaType.DIRECT)
        new_chat.users.append(initiator_user)
        new_chat.users.append(destination_user)

        db_session.add(new_chat)
        db_session.commit()

        return new_chat

    except Exception as error:
        db_session.rollback()
        raise error
