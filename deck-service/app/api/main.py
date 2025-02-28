from core.config import settings
from .deck import router as deck_router
from fastapi import APIRouter


router = APIRouter(
    prefix=settings.api.prefix,
)

router.include_router(
    deck_router,
    prefix=settings.api.decks,
)
