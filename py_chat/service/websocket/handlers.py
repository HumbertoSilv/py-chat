from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from py_chat.models.user import Chat, Message
from py_chat.schemas.message import MessageSchema
from py_chat.service.websocket.manager import WebSocketManager

socket_manager = WebSocketManager()


@socket_manager.handler('new_message')
async def new_message(
    incoming_message: dict,
    user_id: str,
    db_session: AsyncSession,
    chats: List[Chat],
):
    message_schema = MessageSchema(**incoming_message)

    new_message = Message(
        content=message_schema.content,
        user_id=user_id,
        chat_id=message_schema.chat_id,
    )

    db_session.add(new_message)
    await db_session.commit()

    await socket_manager.broadcast_to_chat(
        message_schema.chat_id, incoming_message
    )
