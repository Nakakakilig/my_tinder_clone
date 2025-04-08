from contextlib import asynccontextmanager

import uvicorn
from exception_handler import add_exception_handler
from fastapi import FastAPI

from config.settings import settings
from infrastructure.db.db_helper import db_helper
from infrastructure.kafka.init import init_kafka_producer, stop_kafka_producer
from presentation.routes.main import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await init_kafka_producer()
    yield
    # shutdown
    print("dispose engine")
    await db_helper.dispose()
    print("stop kafka producer")
    await stop_kafka_producer()


app = FastAPI(lifespan=lifespan)
app = add_exception_handler(app)
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
