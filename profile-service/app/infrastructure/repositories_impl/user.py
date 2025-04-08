from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.user import User
from domain.repositories.user import IUserRepository
from infrastructure.db.db_models import UserORM


class UserRepositoryImpl(IUserRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_user_by_id(self, user_id: int) -> User | None:
        stmt = select(UserORM).where(UserORM.id == user_id)
        result = await self.db_session.execute(stmt)
        user_orm = result.scalar_one_or_none()
    async def get_user_by_username(self, username: str) -> User | None:
        stmt = select(UserORM).where(UserORM.username == username)
        result = await self.db_session.execute(stmt)
        user_orm = result.scalar_one_or_none()
        if user_orm is None:
            return None
        return orm_to_domain(user_orm)

    async def create_user(self, user: User) -> User:
        user_orm = UserORM(**user.model_dump())
        self.db_session.add(user_orm)
        await self.db_session.commit()
        await self.db_session.refresh(user_orm)
        return user_orm

    async def get_users(self) -> list[User]:
        stmt = select(UserORM).order_by(UserORM.id)
        result = await self.db_session.execute(stmt)
        users_orm = result.scalars().all()
        return users_orm
