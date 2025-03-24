from typing import AsyncGenerator

from application.services.preference import PreferenceService
from fastapi import Depends
from infrastructure.db.db_helper import db_helper
from infrastructure.kafka.init import get_kafka_producer
from infrastructure.kafka.producer import KafkaProducer
from infrastructure.repositories_impl.preference import PreferenceRepositoryImpl
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in db_helper.session_getter():
        yield session


def get_preference_service(
    db_session: AsyncSession = Depends(get_db_session),
    kafka_producer: KafkaProducer = Depends(get_kafka_producer),
) -> PreferenceService:
    preference_repository = PreferenceRepositoryImpl(db_session)
    return PreferenceService(preference_repository, kafka_producer)
