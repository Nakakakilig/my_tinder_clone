import json
from datetime import datetime

from aiokafka import AIOKafkaProducer
from core.config import settings
from core.schemas.profile import ProfileCreate
from enum import Enum


producer: AIOKafkaProducer | None = None


async def init_kafka_producer():
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.kafka.bootstrap_servers,
        value_serializer=lambda v: json.dumps(
            v, default=lambda x: x.value if isinstance(x, Enum) else str(x)
        ).encode("utf-8"),
    )
    await producer.start()


async def shutdown_kafka_producer():
    global producer
    if producer:
        await producer.stop()


async def publish_profile_created_event(
    profile_create: ProfileCreate,
):
    event = {
        "event_type": "profile_created",
        "data": {
            **profile_create.model_dump(exclude={"user_id"}),
        },
        "timestamp": datetime.now().isoformat(),
    }

    await producer.send_and_wait(settings.kafka.profile_topic, event)
