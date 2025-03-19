# import json
# from enum import Enum

# from aiokafka import AIOKafkaProducer

# from app.core.config import settings
# from app.core.schemas.preferences import PreferenceCreate
# from app.core.schemas.profile import ProfileCreate
# from app.utils.kafka_helper import sync_with_deck_service

# producer: AIOKafkaProducer | None = None


# async def init_kafka_producer():
#     global producer
#     producer = AIOKafkaProducer(
#         bootstrap_servers=settings.kafka.bootstrap_servers,
#         value_serializer=lambda v: json.dumps(
#             v, default=lambda x: x.value if isinstance(x, Enum) else str(x)
#         ).encode("utf-8"),
#     )
#     await producer.start()


# async def shutdown_kafka_producer():
#     global producer
#     if producer:
#         await producer.stop()


# async def publish_profile_created_event(
#     profile_create: ProfileCreate,
# ):
#     await sync_with_deck_service(
#         producer,
#         event_type="profile_created",
#         data={**profile_create.model_dump()},
#         topic=settings.kafka.profile_topic,
#     )


# async def publish_preference_created_event(
#     preference_create: PreferenceCreate,
# ):
#     await sync_with_deck_service(
#         producer,
#         event_type="preference_created",
#         data={**preference_create.model_dump()},
#         topic=settings.kafka.profile_topic,
#     )


import json
from enum import Enum

from aiokafka import AIOKafkaProducer
from pydantic import BaseModel
# from config.settings import settings


class KafkaProducer:
    def __init__(self, bootstrap_servers: str):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(
                v, default=lambda x: x.value if isinstance(x, Enum) else str(x)
            ).encode("utf-8"),
        )

    async def start(self):
        if not self.producer:
            await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def send_event(self, topic: str, event: BaseModel):
        message = json.dumps(event.model_dump(), default=str).encode("utf-8")
        await self.producer.send(topic, message)
