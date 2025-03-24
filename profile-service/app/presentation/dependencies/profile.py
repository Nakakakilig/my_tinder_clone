from typing import AsyncGenerator

from application.services.profile import ProfileService
from fastapi import Depends
from infrastructure.db.db_helper import db_helper
from infrastructure.kafka.init import get_kafka_producer
from infrastructure.kafka.producer import KafkaProducer
from infrastructure.repositories_impl.profile import ProfileRepositoryImpl
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in db_helper.session_getter():
        yield session


def get_profile_service(
    db_session: AsyncSession = Depends(get_db_session),
    kafka_producer: KafkaProducer = Depends(get_kafka_producer),
) -> ProfileService:
    profile_repository = ProfileRepositoryImpl(db_session)
    return ProfileService(profile_repository, kafka_producer)
