from py_chat.models.user import Chat
from py_chat.schemas.message import MessageSchema
from py_chat.service.websocket.manager import WebSocketManager

socket_manager = WebSocketManager()


@socket_manager.handler('new_message')
async def new_message(
    incoming_message: dict,
    chats: Chat,
):
    message_schema = MessageSchema(**incoming_message)
    chat_id = str(message_schema.chat_id)

    await socket_manager.broadcast_to_chat(chat_id, incoming_message)
