from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from py_chat.api.dependencies import get_current_user
from py_chat.core.database import get_async_session
from py_chat.models.user import User
from py_chat.schemas.chat import ChatId, ChatPublic, ChatSchema
from py_chat.service.chat import (
    create_direct_chat,
    get_latest_chat_message,
    get_user_chats,
)

router = APIRouter(prefix='/chats', tags=['Chats'])

T_Session = Annotated[AsyncSession, Depends(get_async_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/direct',
    status_code=HTTPStatus.CREATED,
    response_model=ChatId,
)
async def create_direct_chat_(
    session: T_Session,
    create_direct_chat_schema: ChatSchema,
    current_user: T_CurrentUser,
):
    stmt = select(User).where(
        User.id == create_direct_chat_schema.destination_user_id
    )
    result = await session.execute(stmt)
    destination_user = result.scalars().first()

    initiator_user = await session.get(User, current_user.id)

    if not destination_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Destination not found',
        )

    # TODO: if direct_chat_exists

    new_chat = await create_direct_chat(
        session=session,
        destination_user=destination_user,
        initiator_user=initiator_user,
    )

    return new_chat


@router.get(
    '/direct', status_code=HTTPStatus.OK, response_model=list[ChatPublic]
)
async def list_direct_chats(session: T_Session, current_user: T_CurrentUser):
    chats = await get_user_chats(session, current_user.id)

    response = []
    for chat in chats:
        last_message = await get_latest_chat_message(session, chat.id)

        chat_public = {
            'id': chat.id,
            'chat_type': chat.chat_type.value,
            'users': chat.users,
            'last_message': last_message,
        }
        response.append(chat_public)

    return response
