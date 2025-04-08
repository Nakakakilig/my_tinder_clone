from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.repositories_impl.user import UserRepositoryImpl
from presentation.dependencies.db_session import get_db_session
from use_cases.user import UserService


def get_user_service(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> UserService:
    user_repository = UserRepositoryImpl(db_session)
    return UserService(user_repository)
