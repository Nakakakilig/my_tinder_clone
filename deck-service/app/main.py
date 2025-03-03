import uvicorn
from core.config import settings
from api.main import router as deck_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(deck_router)

# TODO: add redis connect/shutdown to lifespan

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
