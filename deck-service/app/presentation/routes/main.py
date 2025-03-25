from config.settings import settings
from fastapi import APIRouter
from presentation.routes.deck import router as deck_router
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
