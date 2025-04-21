from aiokafka.errors import KafkaConnectionError  # type: ignore

from config.settings import settings
from infrastructure.kafka.producer import KafkaProducer

# Global variable to store the Kafka producer instance
kafka_producer: KafkaProducer | None = None


async def init_kafka_producer() -> KafkaProducer:
    try:
        global kafka_producer  # noqa: PLW0603
        if kafka_producer is None:
            kafka_producer = KafkaProducer(bootstrap_servers=settings.kafka.bootstrap_servers)
            await kafka_producer.start()
        return kafka_producer  # noqa: TRY300
    except KafkaConnectionError as e:
        raise KafkaConnectionError() from e


async def stop_kafka_producer() -> None:
    global kafka_producer  # noqa: PLW0603
    if kafka_producer:
        await kafka_producer.stop()
        kafka_producer = None


def get_kafka_producer() -> KafkaProducer:
    global kafka_producer  # noqa: PLW0602
    if kafka_producer is None:
        raise KafkaConnectionError(  # noqa: TRY003
            "Kafka producer is not initialized. Call init_kafka_producer() first."
        )
    return kafka_producer
