from typing import AsyncGenerator

from application.services.user import UserService
from fastapi import Depends
from infrastructure.db.db_helper import db_helper
from infrastructure.repositories_impl.user import UserRepositoryImpl
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in db_helper.session_getter():
        yield session


def get_user_service(db_session: AsyncSession = Depends(get_db_session)) -> UserService:
    user_repository = UserRepositoryImpl(db_session)
    return UserService(user_repository)
