import asyncio
import random

from application.schemas.profile import ProfileCreate
from domain.enums import Gender
from faker import Faker
from infrastructure.db.db_helper import db_helper
from presentation.dependencies.profile import get_profile_service

fake = Faker("uk_UA")

# APPROXIMATE BOUNDARIES OF UKRAINE
TOP_RIGHT_LATITUDE = 52.16
TOP_RIGHT_LONGITUDE = 22.00
BOTTOM_LEFT_LATITUDE = 44.80
BOTTOM_LEFT_LONGITUDE = 40.12


async def create_multiple_profiles(
    # producer: AIOKafkaProducer,
    N_profiles: int = 100,
):
    profile_creates = [
        ProfileCreate(
            user_id=i,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            gender=random.choice(list(Gender)),
            age=random.randint(18, 60),
            geo_latitude=random.uniform(BOTTOM_LEFT_LATITUDE, TOP_RIGHT_LATITUDE),
            geo_longitude=random.uniform(BOTTOM_LEFT_LONGITUDE, TOP_RIGHT_LONGITUDE),
        )
        for i in range(1, N_profiles + 1)
    ]

    await asyncio.sleep(5)

    async for session in db_helper.session_getter():
        for profile_create in profile_creates:
            await get_profile_service(session).create_profile(profile_create)

            # await sync_with_deck_service(
            #     producer,
            #     event_type="profile_created",
            #     data={**profile_create.model_dump()},
            #     topic="profile-events",
            # )

    print(f"Created {N_profiles} profiles")
