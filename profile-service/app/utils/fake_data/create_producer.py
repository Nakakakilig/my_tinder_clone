import json
import os
import sys
from enum import Enum

from aiokafka import AIOKafkaProducer

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))  # for core
)
from app.core.config import settings

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
    return producer
