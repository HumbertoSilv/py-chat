from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from py_chat.api.dependencies import get_current_user
from py_chat.core.database import get_session
from py_chat.models.user import User
from py_chat.schemas.schemas import ChatSchema, CreateDirectChatSchema, PublicDirectChatSchema
from py_chat.service.chat import create_direct_chat, get_user_chats

router = APIRouter(prefix='/chats', tags=['chats'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[str | None, Depends(get_current_user)]


@router.post('/direct', status_code=HTTPStatus.CREATED, response_model=PublicDirectChatSchema)
async def create_direct_chat_(
    db_session: T_Session,
    create_direct_chat_schema: CreateDirectChatSchema,
    current_user: T_CurrentUser
):
    destination_user = db_session.scalar(
        select(User).where(
            User.id == create_direct_chat_schema.destination_user_id
        )
    )

    initiator_user = db_session.scalar(
        select(User).where(
            User.id == current_user
        )
    )

    if not destination_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Not found",
        )

    # TODO: if direct_chat_exists

    new_chat = create_direct_chat(
        db_session=db_session,
        destination_user=destination_user,
        initiator_user=initiator_user
    )

    return new_chat


@router.get('/direct', status_code=HTTPStatus.OK, response_model=list[ChatSchema])
def list_direct_chats(
    db_session: T_Session,
    user_id: T_CurrentUser
):
    chats = get_user_chats(db_session, user_id)

    for chat in chats:
        chat.users = [
            user for user in chat.users if str(user.id) != user_id
        ]

    return chats
