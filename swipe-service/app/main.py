from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.main import router
from app.core.config import settings
from app.core.db.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    print("dispose engine")
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(
    router,
)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
