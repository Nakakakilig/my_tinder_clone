from fastapi import APIRouter

from app.api.deck import router as deck_router
from app.api.profile import router as profile_router
from app.core.config import settings

router = APIRouter(
    prefix=settings.api.prefix,
)

router.include_router(
    deck_router,
    prefix=settings.api.decks,
)

router.include_router(
    profile_router,
    prefix="/profiles",
)
