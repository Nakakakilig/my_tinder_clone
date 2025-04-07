import asyncio
import json
from time import sleep

from aiokafka import AIOKafkaConsumer  # type: ignore
from aiokafka.errors import KafkaConnectionError  # type: ignore

from config.settings import settings
from infrastructure.kafka.events import handle_event


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
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),  # type: ignore
    )
    consume_started = False
    while not consume_started:
        try:
            await consumer.start()
            consume_started = True
        except KafkaConnectionError:
            consume_started = False
            print("CONSUMER CANT START. SLEEP FOR 5 SECONDS")
            # yes, its a bad practice, but i need here for easy debugging
            sleep(5)  # noqa: ASYNC251

    try:
        print("Kafka consumer started and listening...")
        async for message in consumer:  # type: ignore
            event = message.value  # type: ignore
            await handle_event(event)  # type: ignore
    finally:
        await consumer.stop()  # type: ignore


async def start_consumer_loop():
    loop = asyncio.get_event_loop()
    loop.create_task(consume())  # noqa: RUF006
