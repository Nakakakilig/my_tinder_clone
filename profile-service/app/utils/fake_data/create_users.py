import asyncio

from application.schemas.user import UserCreate
from faker import Faker
from infrastructure.db.db_helper import db_helper
from presentation.dependencies.user import get_user_service

fake = Faker("uk_UA")


async def create_multiple_users(N_users: int = 100):
    user_creates = [
        UserCreate(username=fake.user_name()) for _ in range(1, N_users + 1)
    ]

    await asyncio.sleep(5)

    async for session in db_helper.session_getter():
        for user_create in user_creates:
            await get_user_service(session).create_user(user_create)

    print(f"Successfully created {len(user_creates)} users")
