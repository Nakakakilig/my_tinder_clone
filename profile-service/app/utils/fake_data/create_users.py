from core.db.db_helper import db_helper
from core.models.user import User
from core.schemas.user import UserCreate
from faker import Faker

fake = Faker("uk_UA")


async def create_multiple_users(N_users: int = 100):
    user_creates = [
        UserCreate(username=fake.user_name()) for _ in range(1, N_users + 1)
    ]

    async for session in db_helper.session_getter():
        users = [User(**user_create.model_dump()) for user_create in user_creates]
        session.add_all(users)
        await session.commit()
        print(f"Successfully created {len(users)} users")
