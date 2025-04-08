from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.repositories_impl.profile import ProfileRepositoryImpl
from presentation.dependencies.db_session import get_db_session
from use_cases.profile import ProfileService


def get_profile_service(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> ProfileService:
    profile_repository = ProfileRepositoryImpl(db_session)
    return ProfileService(profile_repository)
