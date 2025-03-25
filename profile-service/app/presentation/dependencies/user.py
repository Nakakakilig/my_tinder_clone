from application.services.user import UserService
from fastapi import Depends
from infrastructure.repositories_impl.user import UserRepositoryImpl
from presentation.dependencies.db_session import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession


def get_user_service(
    db_session: AsyncSession = Depends(get_db_session),
) -> UserService:
    user_repository = UserRepositoryImpl(db_session)
    return UserService(user_repository)
