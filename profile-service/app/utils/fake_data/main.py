import asyncio

from infrastructure.kafka.init import init_kafka_producer, stop_kafka_producer

from .create_preferences import create_multiple_preferences
from .create_profiles import create_multiple_profiles
from .create_users import create_multiple_users

N_USERS = 100


async def main():
    await init_kafka_producer()

    try:
        await create_multiple_users(N_USERS)
        await create_multiple_profiles(N_USERS)
        await create_multiple_preferences(N_USERS)
    finally:
        await stop_kafka_producer()


if __name__ == "__main__":
    asyncio.run(main())
