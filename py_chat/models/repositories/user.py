from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from py_chat.models.repositories.interfaces.user import UserRepositoryInterface
from py_chat.models.user import User
from py_chat.schemas.user import UserUpdateSchema


class UserRepository(UserRepositoryInterface):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, username: str, email: str) -> User:
        user = User(username=username, email=email)
        await user.save(self.db_session)
        return user

    async def get_user_by_ID(self, user_id: UUID) -> User | None:
        result = await self.db_session.get(User, user_id)
        return result

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.db_session.execute(stmt)

        return result.scalars().first()

    async def get_user_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await self.db_session.execute(stmt)

        return result.scalars().first()

    async def update_user(
        self, user_id: UUID, payload: UserUpdateSchema
    ) -> None:
        user = await self.db_session.get(User, user_id)

        await user.update(
            self.db_session, **payload.model_dump(exclude_none=True)
        )
