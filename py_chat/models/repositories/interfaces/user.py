from abc import ABC, abstractmethod
from uuid import UUID

from py_chat.models.user import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    async def create_user(self, username: str, email: str) -> User:
        """Create a new user"""
        pass  # pragma: no cover

    @abstractmethod
    async def get_user_by_ID(self, user_id: UUID) -> User | None:
        """Get user by ID"""
        pass  # pragma: no cover

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User | None:
        """Get user by username"""
        pass  # pragma: no cover

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        """Get user by email"""
        pass  # pragma: no cover

    @abstractmethod
    async def update_user(self, user_id: UUID, **kwargs) -> None:
        """Update user information"""
        pass  # pragma: no cover

    @abstractmethod
    async def search_username_by_query(self, query: str) -> list[User]:
        """Search users by username query"""
        pass  # pragma: no cover
