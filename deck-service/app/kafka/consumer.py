from aiokafka import AIOKafkaConsumer
import json
import asyncio
from core.config import settings
from kafka.events import handle_event


async def consume():
    """
    Start consuming messages from Kafka topic.

    The consumer is part of a group and will automatically commit
    messages as they are consumed.
    """

    bootstrap_servers = settings.kafka.bootstrap_servers
    topic = settings.kafka.profile_topic
    group_id = "deck-service-group"

    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )
    await consumer.start()

    try:
        print("Kafka consumer started and listening...")
        async for message in consumer:
            event = message.value
            await handle_event(event)
    finally:
        await consumer.stop()


async def start_consumer_loop():
    loop = asyncio.get_event_loop()
    loop.create_task(consume())
