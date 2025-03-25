from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from config.settings import settings
from infrastructure.kafka.consumer import start_consumer_loop
from presentation.routes.main import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_consumer_loop()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)

# TODO: add redis connect/shutdown to lifespan

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
