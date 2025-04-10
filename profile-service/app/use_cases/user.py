import logging

from domain.models.user import User
from domain.repositories.user import IUserRepository

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def create_user(self, user: User) -> User:
        logger.info("Creating user: %s", user.username)
        created_user = await self.user_repository.create_user(user)
        logger.info("User created: %s", created_user.username)
        return created_user

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.user_repository.get_user_by_id(user_id)

    async def get_user_by_username(self, username: str) -> User | None:
        return await self.user_repository.get_user_by_username(username)

    async def get_users(self, limit: int, offset: int) -> list[User] | None:
        return await self.user_repository.get_users(limit, offset)
