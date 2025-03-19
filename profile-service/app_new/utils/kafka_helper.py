from datetime import datetime
from typing import Any
from aiokafka import AIOKafkaProducer


async def sync_with_deck_service(
    producer: AIOKafkaProducer,
    event_type: str,
    data: dict[str, Any],
    topic: str,
) -> None:
    """General function to sync profile-service data with deck service."""
    fake_event = {
        "event_type": event_type,
        "data": data,
        "timestamp": datetime.now().isoformat(),
    }

    await producer.send_and_wait(topic, fake_event)
