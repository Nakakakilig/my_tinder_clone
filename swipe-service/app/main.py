from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from config.settings import settings
from infrastructure.db.db_helper import db_helper
from presentation.routes.main import router


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
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
