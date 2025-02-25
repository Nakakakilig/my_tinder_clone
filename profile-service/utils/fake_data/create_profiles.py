import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from core.db.db_helper import db_helper
from core.db.enums import Gender
from core.models.profile import Profile
from core.schemas.profile import ProfileCreate
from faker import Faker

fake = Faker("uk_UA")

TOP_RIGHT_LATITUDE = 52.16
TOP_RIGHT_LONGITUDE = 22.00

BOTTOM_LEFT_LATITUDE = 44.80
BOTTOM_LEFT_LONGITUDE = 40.12


async def create_multiple_profiles(N_profiles: int = 100):
    profile_creates = [
        ProfileCreate(
            user_id=i,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            gender=random.choice(list(Gender)),
            geo_latitude=random.uniform(BOTTOM_LEFT_LATITUDE, TOP_RIGHT_LATITUDE),
            geo_longitude=random.uniform(BOTTOM_LEFT_LONGITUDE, TOP_RIGHT_LONGITUDE),
        )
        for i in range(1, N_profiles + 1)
    ]

    async for session in db_helper.session_getter():
        profiles = [
            Profile(**profile_create.model_dump()) for profile_create in profile_creates
        ]
        session.add_all(profiles)
        await session.commit()
        print(f"Successfully created {len(profiles)} profiles")
