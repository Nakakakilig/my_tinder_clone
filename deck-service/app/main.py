from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.main import router as deck_router
from app.core.config import settings
from app.kafka.consumer import start_consumer_loop


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_consumer_loop()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(deck_router)

# TODO: add redis connect/shutdown to lifespan

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
