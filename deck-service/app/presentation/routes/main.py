from fastapi import APIRouter

from config.settings import settings
from presentation.routes.deck import router as deck_router
from presentation.routes.preference import router as preference_router
from presentation.routes.profile import router as profile_router

router = APIRouter(
    prefix=settings.api.prefix,
)

router.include_router(
    deck_router,
    prefix=settings.api.decks,
)

router.include_router(
    profile_router,
    prefix=settings.api.profiles,
)

router.include_router(
    preference_router,
    prefix=settings.api.preferences,
)
