from fastapi import APIRouter

from presentation.routes.swipe import router as swipe_router
from config.settings import settings

router = APIRouter(
    prefix=settings.api.prefix,
)

router.include_router(
    swipe_router,
    prefix=settings.api.swipes,
)
