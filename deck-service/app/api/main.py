from core.config import settings
from .deck import router as deck_router
from .profile import router as profile_router
from fastapi import APIRouter


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
