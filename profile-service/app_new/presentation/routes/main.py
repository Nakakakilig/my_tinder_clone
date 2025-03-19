from fastapi import APIRouter

from app.api.preference import router as preference_router
from app.api.profiles import router as profile_router
from app.api.users import router as user_router
from app.core.config import settings

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
