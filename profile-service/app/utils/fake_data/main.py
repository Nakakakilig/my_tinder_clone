import asyncio
import json
import os
import sys
from enum import Enum

from aiokafka import AIOKafkaProducer
from create_preferences import create_multiple_preferences
from create_profiles import create_multiple_profiles
from create_users import create_multiple_users

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))  # for core
)
from core.config import settings

N_USERS = 100


async def init_kafka_producer():
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.kafka.bootstrap_servers,
        value_serializer=lambda v: json.dumps(
            v, default=lambda x: x.value if isinstance(x, Enum) else str(x)
        ).encode("utf-8"),
    )
    await producer.start()
    return producer


async def main():
    producer = await init_kafka_producer()

    await create_multiple_users(N_USERS)
    await create_multiple_profiles(
        producer,
        N_USERS,
    )
    await create_multiple_preferences(N_USERS)

    await producer.stop()


if __name__ == "__main__":
    asyncio.run(main())
