import json
from enum import Enum
from typing import Any

from aiokafka import AIOKafkaProducer  # type: ignore


class KafkaProducer:
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self._producer = None

    @property
    def producer(self) -> AIOKafkaProducer:
        if self._producer is None:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(  # type: ignore
                    v, default=lambda x: x.value if isinstance(x, Enum) else str(x)
                ).encode("utf-8"),
            )
        return self._producer

    async def start(self):
        if not self._producer:
            self._producer = self.producer
            await self._producer.start()

    async def stop(self):
        if self._producer:
            await self._producer.stop()
            self._producer = None

    async def send_event(self, topic: str, event: dict[str, Any]):
        if not self._producer:
            await self.start()
        await self.producer.send_and_wait(topic, event)  # type: ignore
