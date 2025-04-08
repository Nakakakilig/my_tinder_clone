import asyncio
import contextlib

from faker import Faker

from domain.exceptions import UserAlreadyExistsError
from domain.models.user import User
from infrastructure.db.db_helper import db_helper
from presentation.dependencies.user import get_user_service
from presentation.schemas.user import UserCreateSchema

fake = Faker("uk_UA")


async def create_multiple_users(n_users: int = 100):
    user_creates = [UserCreateSchema(username=fake.user_name()) for _ in range(1, n_users + 1)]

    await asyncio.sleep(5)

    async for session in db_helper.session_getter():
        for user_create in user_creates:
            user = User(**user_create.model_dump())
            user_service = get_user_service(session)
            with contextlib.suppress(UserAlreadyExistsError):  # skip error
                await user_service.create_user(user)
    print(f"Successfully created {len(user_creates)} users")
