from application.services.preference import PreferenceService
from fastapi import Depends
from infrastructure.kafka.init import get_kafka_producer
from infrastructure.kafka.producer import KafkaProducer
from infrastructure.repositories_impl.preference import PreferenceRepositoryImpl
from presentation.dependencies.db_session import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated


def get_preference_service(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    kafka_producer: Annotated[KafkaProducer, Depends(get_kafka_producer)],
) -> PreferenceService:
    preference_repository = PreferenceRepositoryImpl(db_session)
    return PreferenceService(preference_repository, kafka_producer)
