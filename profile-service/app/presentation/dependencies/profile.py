from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.kafka.init import get_kafka_producer
from infrastructure.kafka.producer import KafkaProducer
from infrastructure.repositories_impl.profile import ProfileRepositoryImpl
from presentation.dependencies.db_session import get_db_session
from use_cases.profile import ProfileService


def get_profile_service(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    kafka_producer: Annotated[KafkaProducer, Depends(get_kafka_producer)],
) -> ProfileService:
    profile_repository = ProfileRepositoryImpl(db_session)
    return ProfileService(profile_repository, kafka_producer)
