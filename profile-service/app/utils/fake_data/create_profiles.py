import asyncio
import os
import random
import sys

from aiokafka import AIOKafkaProducer
from faker import Faker

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))  # for core
)

from app.core.db.db_helper import db_helper
from app.core.schemas.enums import Gender
from app.core.schemas.profile import ProfileCreate
from app.services.profile import create_profile_service
from app.utils.kafka_helper import sync_with_deck_service

fake = Faker("uk_UA")

# APPROXIMATE BOUNDARIES OF UKRAINE
TOP_RIGHT_LATITUDE = 52.16
TOP_RIGHT_LONGITUDE = 22.00
BOTTOM_LEFT_LATITUDE = 44.80
BOTTOM_LEFT_LONGITUDE = 40.12


async def create_multiple_profiles(
    producer: AIOKafkaProducer,
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
            await create_profile_service(session, profile_create, need_event=False)

            await sync_with_deck_service(
                producer,
                event_type="profile_created",
                data={**profile_create.model_dump()},
                topic="profile-events",
            )

    print(f"Created {N_profiles} profiles")
