import asyncio
import random

from application.schemas.preference import PreferenceCreate
from domain.enums import Gender
from infrastructure.db.db_helper import db_helper
from presentation.dependencies.preference import get_preference_service


async def create_multiple_preferences(
    # producer: AIOKafkaProducer,
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
            await get_preference_service(session).create_preference(preference_create)

        # await sync_with_deck_service(
        #     producer,
        #     event_type="preference_created",
        #     data={**preference_create.model_dump()},
        #     topic="profile-events",
        # )

    print(f"Created {N_preferences} preferences")
