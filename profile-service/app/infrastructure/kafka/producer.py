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
