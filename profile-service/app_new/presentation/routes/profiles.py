from fastapi import APIRouter

from app.api.deps import db_dependency
from app.core.schemas.profile import ProfileCreate, ProfileRead
from app.services.profile import (
    create_profile_service,
    get_profile_service,
    get_profiles_service,
)

router = APIRouter(tags=["profiles"])


@router.get("/", response_model=list[ProfileRead])
async def get_profiles(
    session: db_dependency,
):
    return await get_profiles_service(session)


@router.post("/", response_model=ProfileRead)
async def create_profile(
    session: db_dependency,
    profile_create: ProfileCreate,
    # TODO in future:  user_id: UUID = Depends(get_user_id_from_JWT_token)
) -> ProfileRead:
    return await create_profile_service(session, profile_create)


@router.get("/{profile_id}", response_model=ProfileRead)
async def get_profile(
    session: db_dependency,
    profile_id: int,
) -> ProfileRead:
    return await get_profile_service(session, profile_id)
