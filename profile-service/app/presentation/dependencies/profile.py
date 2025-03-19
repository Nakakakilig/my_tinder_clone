from typing import AsyncGenerator

from application.services.profile import ProfileService
from fastapi import Depends
from infrastructure.db.db_helper import db_helper
from infrastructure.repositories_impl.profile import ProfileRepositoryImpl
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in db_helper.session_getter():
        yield session


def get_profile_service(
    db_session: AsyncSession = Depends(get_db_session),
) -> ProfileService:
    from main import get_kafka_producer

    kafka_producer = get_kafka_producer()
    profile_repository = ProfileRepositoryImpl(db_session)
    return ProfileService(profile_repository, kafka_producer)
