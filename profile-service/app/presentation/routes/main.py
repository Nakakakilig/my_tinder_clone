from fastapi import APIRouter


from config.settings import settings
from presentation.routes.preference import router as preference_router
from presentation.routes.profiles import router as profile_router
from presentation.routes.user import router as user_router

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
