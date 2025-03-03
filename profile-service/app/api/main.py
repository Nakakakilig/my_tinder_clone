from core.config import settings
from fastapi import APIRouter

from .users import router as user_router
from .profiles import router as profile_router
from .preference import router as preference_router

router = APIRouter(
    prefix=settings.api.prefix,
)

router.include_router(
    user_router,
    prefix=settings.api.users,
)

router.include_router(
    profile_router,
    prefix=settings.api.profiles,
)

router.include_router(
    preference_router,
    prefix=settings.api.preferences,
)
