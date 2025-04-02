from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from py_chat.api.dependencies import decode_token
from py_chat.core.database import get_async_session
from py_chat.service.chat import get_user_chats
from py_chat.service.websocket.handlers import socket_manager

websocket_router = APIRouter(tags=['ws'])

T_Session = Annotated[AsyncSession, Depends(get_async_session)]


@websocket_router.websocket('/ws/')
async def websocket_endpoint(
    websocket: WebSocket,
    db_session: T_Session,
):
    access_token = websocket.cookies.get('access_token')

    if not access_token:
        return

    token_payload = decode_token(access_token)
    user_id = token_payload['sub']

    if not token_payload or not token_payload.get('sub'):
        await websocket.close(code=1008)
        return

    await socket_manager.connect_socket(websocket)

    await socket_manager.add_user_socket_connection(user_id, websocket)

    user_active_chats = await get_user_chats(session=db_session, user=user_id)

    for chat in user_active_chats:
        await socket_manager.add_user_to_chat(chat.id, websocket)

    try:
        while True:
            incoming_message = await websocket.receive_json()

            message_type = incoming_message.get('type')
            handler = socket_manager.handlers.get(message_type)

            await handler(
                incoming_message=incoming_message,
                db_session=db_session,
                chats=user_active_chats,
                user_id=user_id,
            )

    except WebSocketDisconnect:
        for chat in user_active_chats:
            await socket_manager.remove_user_from_chat(chat.id, websocket)

        await socket_manager.remove_user_guid_to_websocket(user_id, websocket)
        print('WebSocketDisconnect')
