import asyncio
import random

from faker import Faker

from application.schemas.profile import ProfileCreateSchema
from application.services.profile import ProfileService
from domain.enums import Gender
from domain.models.profile import Profile
from infrastructure.db.db_helper import db_helper
from infrastructure.kafka.init import get_kafka_producer
from infrastructure.repositories_impl.profile import ProfileRepositoryImpl

fake = Faker("uk_UA")

# APPROXIMATE BOUNDARIES OF UKRAINE
TOP_RIGHT_LATITUDE = 52.16
TOP_RIGHT_LONGITUDE = 22.00
BOTTOM_LEFT_LATITUDE = 44.80
BOTTOM_LEFT_LONGITUDE = 40.12


async def create_multiple_profiles(
    n_profiles: int = 100,
):
    profile_creates = [
        ProfileCreateSchema(
            user_id=i,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            gender=random.choice(list(Gender)),
            age=random.randint(18, 60),
            geo_latitude=random.uniform(BOTTOM_LEFT_LATITUDE, TOP_RIGHT_LATITUDE),
            geo_longitude=random.uniform(BOTTOM_LEFT_LONGITUDE, TOP_RIGHT_LONGITUDE),
        )
        for i in range(1, n_profiles + 1)
    ]

    await asyncio.sleep(5)

    kafka_producer = get_kafka_producer()
    for profile_create in profile_creates:
        async for session in db_helper.session_getter():
            profile = Profile(**profile_create.model_dump())
            profile_service = ProfileService(
                profile_repository=ProfileRepositoryImpl(session),
                kafka_producer=kafka_producer,
            )
            # todo: add exception handling
            await profile_service.create_profile(profile)
    print(f"Created {n_profiles} profiles")
