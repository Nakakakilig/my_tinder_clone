from domain.models.user import User
from domain.repositories.user import IUserRepository


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def create_user(self, user: User) -> User:
        return await self.user_repository.create_user(user)

    async def get_user_by_id(self, user_id: int) -> User:
        return await self.user_repository.get_user_by_id(user_id)

    async def get_users(self) -> list[User]:
        return await self.user_repository.get_users()
