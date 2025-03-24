from config.settings import settings
from infrastructure.kafka.producer import KafkaProducer

# Global variable to store the Kafka producer instance
kafka_producer: KafkaProducer | None = None


async def init_kafka_producer() -> KafkaProducer:
    global kafka_producer
    if kafka_producer is None:
        kafka_producer = KafkaProducer(
            bootstrap_servers=settings.kafka.bootstrap_servers
        )
        await kafka_producer.start()
    return kafka_producer


async def stop_kafka_producer() -> None:
    global kafka_producer
    if kafka_producer:
        await kafka_producer.stop()
        kafka_producer = None


def get_kafka_producer() -> KafkaProducer:
    global kafka_producer
    if kafka_producer is None:
        raise RuntimeError(
            "Kafka producer is not initialized. Call init_kafka_producer() first."
        )
    return kafka_producer
