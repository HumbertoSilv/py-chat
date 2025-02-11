import uuid
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from py_chat.core.database import get_session
from py_chat.models.user import Friend, User
from py_chat.schemas.schemas import FriendList, UserId

router = APIRouter(prefix='/friends', tags=['friends'])

T_Session = Annotated[Session, Depends(get_session)]


@router.post('/{user_id}', status_code=HTTPStatus.NO_CONTENT)
async def add_friend(user_id: uuid.UUID, friend: UserId, session: T_Session):
    new_friendship = session.scalar(
        select(User).where(User.id == uuid.UUID(friend.id))
    )

    if not new_friendship:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    try:
        friendship = Friend(user_id=user_id, friend_id=uuid.UUID(friend.id))

        session.add(friendship)
        session.commit()

        return {}

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Friendship already exists',
        )


@router.get('/{user_id}', response_model=FriendList, status_code=HTTPStatus.OK)
def get_friends(user_id: uuid.UUID, session: T_Session):
    stmt = (
        select(User)
        .join(
            Friend, (User.id == Friend.friend_id) | (User.id == Friend.user_id)
        )
        .where(
            (Friend.user_id == user_id) | (Friend.friend_id == user_id),
            User.id != user_id,  # Avoid returning the user to the friends list
        )
    )

    friends = session.scalars(stmt).all()

    return {'friends': friends}
