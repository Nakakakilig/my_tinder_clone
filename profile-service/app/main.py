from contextlib import asynccontextmanager

import uvicorn
from api.main import router
from core.config import settings
from core.db.db_helper import db_helper
from fastapi import FastAPI
from services.kafka_producer import init_kafka_producer, shutdown_kafka_producer


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await init_kafka_producer()
    yield
    # shutdown
    print("dispose engine")
    await db_helper.dispose()
    print("shutdown kafka producer")
    await shutdown_kafka_producer()


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
