from contextlib import asynccontextmanager

import uvicorn
from api.main import router as profile_router
from core.config import settings
from core.db.db_helper import db_helper
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    print("dispose engine")
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(
    profile_router,
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
