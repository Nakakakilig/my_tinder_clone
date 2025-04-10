from contextlib import asynccontextmanager

import uvicorn
from exception_handler import add_exception_handler
from fastapi import FastAPI

from config.settings import settings
from infrastructure.db.db_helper import db_helper
from infrastructure.middleware import CorrelationIdMiddleware
from presentation.routes.main import router
from utils.logging import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    configure_logging()
    yield
    # shutdown
    print("dispose engine")
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)
app = add_exception_handler(app)
app.add_middleware(CorrelationIdMiddleware)
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
