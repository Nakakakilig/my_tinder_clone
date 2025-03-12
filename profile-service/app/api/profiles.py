from fastapi import APIRouter, HTTPException

from app.api.deps import db_dependency
from app.core.schemas.enums import Gender
from app.core.schemas.profile import ProfileCreate, ProfileRead, ProfileWithDistance
from app.crud import profiles as profiles_crud
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


@router.get("/{profile_id}/matches", response_model=list[ProfileWithDistance])
async def get_matching_profiles(
    session: db_dependency,
    profile_id: int = None,
    gender: Gender | None = None,
    age: int = None,
    radius: int | None = None,
    limit: int | None = 10,
) -> list[dict]:
    matching_profiles = await profiles_crud.get_matching_profiles(
        session=session,
        # TODO: maybe i can paste here PreferenceBase instead a lot of params
        profile_id=profile_id,
        gender=gender,
        age=age,
        radius=radius,
        limit=limit,
    )
    if not matching_profiles:
        raise HTTPException(status_code=404, detail="No matching profiles found")

    return matching_profiles
