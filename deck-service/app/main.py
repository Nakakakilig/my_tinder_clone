from contextlib import asynccontextmanager

import uvicorn
from exception_handler import add_exception_handler
from fastapi import FastAPI

from config.settings import settings
from infrastructure.kafka.consumer import start_consumer_loop
from infrastructure.middleware import CorrelationIdMiddleware
from presentation.routes.main import router
from utils.logging import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await start_consumer_loop()  # type: ignore
    yield


app = FastAPI(lifespan=lifespan)
app = add_exception_handler(app)
app.add_middleware(CorrelationIdMiddleware)
app.include_router(router)

# TODO: add redis connect/shutdown to lifespan

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
