from abc import ABC, abstractmethod

from domain.models.user import User


class IUserRepository(ABC):
    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def create_user(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_users(self, limit: int, offset: int) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User | None:
        raise NotImplementedError
