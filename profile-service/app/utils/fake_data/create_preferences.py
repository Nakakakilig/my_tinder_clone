import asyncio
import os
import random
import sys

from aiokafka import AIOKafkaProducer

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))  # for core
)

from app.core.db.db_helper import db_helper
from app.core.schemas.enums import Gender
from app.core.schemas.preferences import PreferenceCreate
from app.services.preference import create_preference_service
from app.utils.kafka_helper import sync_with_deck_service


async def create_multiple_preferences(
    producer: AIOKafkaProducer,
    N_preferences: int = 100,
):
    preferences_creates = [
        PreferenceCreate(
            profile_id=i,
            gender=random.choice(list(Gender)),
            age=random.randint(18, 60),
            radius=random.randint(0, 400),
        )
        for i in range(1, N_preferences + 1)
    ]

    await asyncio.sleep(5)

    async for session in db_helper.session_getter():
        for preference_create in preferences_creates:
            await create_preference_service(
                session, preference_create, need_event=False
            )

            await sync_with_deck_service(
                producer,
                event_type="preference_created",
                data={**preference_create.model_dump()},
                topic="profile-events",
            )

    print(f"Created {N_preferences} preferences")
