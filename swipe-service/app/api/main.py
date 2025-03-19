from fastapi import APIRouter

from app.api.swipe import router as swipe_router
from app.core.config import settings

router = APIRouter(
    prefix=settings.api.prefix,
)

router.include_router(
    swipe_router,
    prefix=settings.api.swipes,
)
