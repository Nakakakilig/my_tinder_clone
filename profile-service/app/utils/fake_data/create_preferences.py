import asyncio
import random

from application.schemas.preference import PreferenceCreateSchema
from application.services.preference import PreferenceService
from domain.enums import Gender
from infrastructure.db.db_helper import db_helper
from infrastructure.kafka.init import get_kafka_producer
from infrastructure.repositories_impl.preference import PreferenceRepositoryImpl


async def create_multiple_preferences(
    N_preferences: int = 100,
):
    preferences_creates = [
        PreferenceCreateSchema(
            profile_id=i,
            gender=random.choice(list(Gender)),
            age=random.randint(18, 60),
            radius=random.randint(0, 400),
        )
        for i in range(1, N_preferences + 1)
    ]

    await asyncio.sleep(5)

    kafka_producer = get_kafka_producer()
    for preference_create in preferences_creates:
        async for session in db_helper.session_getter():
            preference_service = PreferenceService(
                preference_repository=PreferenceRepositoryImpl(session),
                kafka_producer=kafka_producer,
            )
            await preference_service.create_preference(preference_create)

    print(f"Created {N_preferences} preferences")
