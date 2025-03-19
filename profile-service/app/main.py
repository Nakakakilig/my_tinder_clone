from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from config.settings import settings
from infrastructure.db.db_helper import db_helper
from infrastructure.kafka.producer import KafkaProducer
from presentation.routes.main import router

kafka_producer = KafkaProducer(bootstrap_servers=settings.kafka.bootstrap_servers)


def get_kafka_producer() -> KafkaProducer:
    return kafka_producer


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await kafka_producer.start()
    yield
    # shutdown
    print("dispose engine")
    await db_helper.dispose()
    print("stop kafka producer")
    await kafka_producer.stop()


app = FastAPI(lifespan=lifespan)
app.include_router(
    router,
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
