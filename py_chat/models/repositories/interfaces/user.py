from abc import ABC, abstractmethod
from uuid import UUID

from py_chat.models.user import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    async def create_user(self, username: str, email: str) -> User:
        """Create a new user"""
        pass

    @abstractmethod
    async def get_user_by_ID(self, user_id: UUID) -> User | None:
        """Get user by ID"""
        pass

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User | None:
        """Get user by username"""
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        """Get user by email"""
        pass

    @abstractmethod
    async def update_user(self, user_id: UUID, **kwargs) -> None:
        """Update user information"""
        pass
