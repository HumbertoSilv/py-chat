from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from py_chat.api.dependencies import get_current_user
from py_chat.core.database import get_async_session
from py_chat.models.user import Friend, User
from py_chat.schemas.friend import FriendListPublic
from py_chat.schemas.user import UserId

router = APIRouter(prefix='/friends', tags=['Friends'])

T_Session = Annotated[AsyncSession, Depends(get_async_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/add', status_code=HTTPStatus.NO_CONTENT)
async def add_friend(
    session: T_Session, current_user: T_CurrentUser, friend: UserId
):
    new_friendship = await session.get(User, friend.id)

    if not new_friendship:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    try:
        friendship = Friend(user_id=current_user.id, friend_id=friend.id)

        session.add(friendship)
        await session.commit()

        return {}

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Friendship already exists',
        )


@router.get(
    '/list', response_model=FriendListPublic, status_code=HTTPStatus.OK
)
async def get_friends(current_user: T_CurrentUser, session: T_Session):
    stmt = (
        select(User)
        .join(
            Friend, (User.id == Friend.friend_id) | (User.id == Friend.user_id)
        )
        .where(
            (Friend.user_id == current_user.id)
            | (Friend.friend_id == current_user.id),
            User.id
            != current_user.id,  # Avoid returning the user to the friends list
        )
    )

    result = await session.execute(stmt)
    friends = result.scalars().all()

    return {'friends': friends}
