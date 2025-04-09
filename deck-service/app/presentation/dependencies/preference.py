from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.repositories_impl.preference import PreferenceRepositoryImpl
from presentation.dependencies.db_session import get_db_session
from use_cases.preference import PreferenceService


def get_preference_service(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> PreferenceService:
    preference_repository = PreferenceRepositoryImpl(db_session)
    return PreferenceService(preference_repository)
