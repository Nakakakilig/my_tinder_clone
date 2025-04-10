import json
from enum import Enum
from typing import Any

import logging
from aiokafka import AIOKafkaProducer  # type: ignore

from infrastructure.middleware import get_correlation_id

logger = logging.getLogger(__name__)


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
            await self._producer.stop()  # type: ignore
            self._producer = None

    async def send_event(self, topic: str, event: dict[str, Any]):
        if not self._producer:
            await self.start()

        headers = [
            ("X-Correlation-Id", get_correlation_id().encode("utf-8")),
        ]
        logger.info("Sending event to topic: %s", topic)
        try:
            await self.producer.send_and_wait(  # type: ignore
                topic,
                event,
                headers=headers,
            )
            logger.info("Event sent to topic: %s", topic)
        except Exception as e:
            logger.exception(f"Error sending event to topic: {topic}")
            raise e  # noqa: TRY201
