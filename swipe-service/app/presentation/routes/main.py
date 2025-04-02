from fastapi import APIRouter

from config.settings import settings
from presentation.routes.swipe import router as swipe_router

router = APIRouter(
    prefix=settings.api.prefix,
)

router.include_router(
    swipe_router,
    prefix=settings.api.swipes,
)
