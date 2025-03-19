import asyncio

# from app.utils.fake_data.create_preferences import create_multiple_preferences
# from app.utils.fake_data.create_producer import init_kafka_producer
# from app.utils.fake_data.create_profiles import create_multiple_profiles
# from app.utils.fake_data.create_users import create_multiple_users

from .create_preferences import create_multiple_preferences
from .create_profiles import create_multiple_profiles
from .create_users import create_multiple_users

N_USERS = 100


async def main():
    # producer = await init_kafka_producer()

    await create_multiple_users(N_USERS)
    await create_multiple_profiles(
        # producer,
        N_USERS,
    )
    await create_multiple_preferences(
        # producer,
        N_USERS,
    )

    # await producer.stop()


if __name__ == "__main__":
    asyncio.run(main())
