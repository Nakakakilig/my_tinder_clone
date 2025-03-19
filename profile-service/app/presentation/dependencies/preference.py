from typing import AsyncGenerator

from application.services.preference import PreferenceService
from fastapi import Depends
from infrastructure.db.db_helper import db_helper
from infrastructure.repositories_impl.preference import PreferenceRepositoryImpl
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in db_helper.session_getter():
        yield session


def get_preference_service(
    db_session: AsyncSession = Depends(get_db_session),
) -> PreferenceService:
    from main import get_kafka_producer

    kafka_producer = get_kafka_producer()
    preference_repository = PreferenceRepositoryImpl(db_session)
    return PreferenceService(preference_repository, kafka_producer)
