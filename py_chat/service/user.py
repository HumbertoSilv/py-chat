from http import HTTPStatus

from fastapi import HTTPException

from py_chat.core.logger import logger
from py_chat.models.repositories.interfaces.user import UserRepositoryInterface
from py_chat.models.user import User
from py_chat.schemas.user import CreateUserSchema


async def create_user(
    user_repository: UserRepositoryInterface, payload: CreateUserSchema
) -> User:
    logger.debug('Start create user: {}', payload)

    if await user_repository.get_user_by_email(payload.email):
        logger.debug('Email already exists')
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Email already exists',
        )

    if await user_repository.get_user_by_username(payload.username):
        logger.debug('Username already exists')
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Username already exists',
        )

    new_user = await user_repository.create_user(**payload.model_dump())
    logger.debug('User created: {}', new_user.id)

    return new_user


async def search_users_by_username(
    user_repository: UserRepositoryInterface, query: str
) -> list[User]:
    logger.debug('Start search user by username: {}', query)

    if not query:
        return []

    list_of_users = await user_repository.search_username_by_query(query)
    logger.debug('Found users: {}', list_of_users)

    return list_of_users
