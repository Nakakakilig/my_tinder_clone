from application.services.preference import PreferenceService
from fastapi import Depends
from infrastructure.repositories_impl.preference import PreferenceRepositoryImpl
from presentation.dependencies.db_session import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession


def get_preference_service(
    db_session: AsyncSession = Depends(get_db_session),
) -> PreferenceService:
    preference_repository = PreferenceRepositoryImpl(db_session)
    return PreferenceService(preference_repository)
