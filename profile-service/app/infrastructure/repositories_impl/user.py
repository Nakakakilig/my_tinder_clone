from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.exceptions import UserAlreadyExistsError, UserCreateError, UserNotFoundError
from domain.models.user import User
from domain.repositories.user import IUserRepository
from infrastructure.db.db_models import UserORM
from infrastructure.mappers.user import domain_to_orm, orm_to_domain


class UserRepositoryImpl(IUserRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_user_by_id(self, user_id: int) -> User | None:
        try:
            stmt = select(UserORM).where(UserORM.id == user_id)
            result = await self.db_session.execute(stmt)
            user_orm = result.scalar_one_or_none()
            if user_orm is None:
                return None
            return orm_to_domain(user_orm)
        except ConnectionRefusedError as e:
            raise ConnectionRefusedError() from e
        except Exception as e:
            raise UserNotFoundError(user_id=user_id) from e

    async def get_user_by_username(self, username: str) -> User | None:
        try:
            stmt = select(UserORM).where(UserORM.username == username)
            result = await self.db_session.execute(stmt)
            user_orm = result.scalar_one_or_none()
            if user_orm is None:
                return None
            return orm_to_domain(user_orm)
        except ConnectionRefusedError as e:
            raise ConnectionRefusedError() from e
        except Exception as e:
            raise UserNotFoundError(username=username) from e

    async def create_user(self, user: User) -> User:
        try:
            if await self.get_user_by_username(user.username):
                raise UserAlreadyExistsError(user.username)
            user_orm = domain_to_orm(user)
            self.db_session.add(user_orm)
            await self.db_session.commit()
            await self.db_session.refresh(user_orm)
            return orm_to_domain(user_orm)
        except ConnectionRefusedError as e:
            raise ConnectionRefusedError() from e
        except Exception as e:
            raise UserCreateError(user.username) from e

    async def get_users(self, limit: int, offset: int) -> list[User]:
        try:
            stmt = select(UserORM).order_by(UserORM.id).limit(limit).offset(offset)
            result = await self.db_session.execute(stmt)
            users_orm = result.scalars().all()
            return [orm_to_domain(user_orm) for user_orm in users_orm]
        except ConnectionRefusedError as e:
            raise ConnectionRefusedError() from e
        except Exception as e:
            raise UserNotFoundError() from e
