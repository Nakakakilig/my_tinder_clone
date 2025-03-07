import random

from core.db.db_helper import db_helper
from core.models.preference import Preference
from core.schemas.enums import Gender
from core.schemas.preferences import PreferenceCreate


async def create_multiple_preferences(N_preferences: int = 100):
    preferences_creates = [
        PreferenceCreate(
            profile_id=i,
            gender=random.choice(list(Gender)),
            age=random.randint(18, 60),
            radius=random.randint(0, 400),
        )
        for i in range(1, N_preferences + 1)
    ]

    async for session in db_helper.session_getter():
        preferences = [
            Preference(**preferences_create.model_dump())
            for preferences_create in preferences_creates
        ]
        session.add_all(preferences)
        await session.commit()
        print(f"Successfully created {len(preferences)} preferences")
