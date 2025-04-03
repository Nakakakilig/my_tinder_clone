from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.services.profile import ProfileService
from infrastructure.repositories_impl.profile import ProfileRepositoryImpl
from presentation.dependencies.db_session import get_db_session


def get_profile_service(
    db_session: AsyncSession = Depends(get_db_session),
) -> ProfileService:
    profile_repository = ProfileRepositoryImpl(db_session)
    return ProfileService(profile_repository)
