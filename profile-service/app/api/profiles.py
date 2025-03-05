from api.deps import db_dependency
from crud import profiles as profiles_crud
from fastapi import APIRouter, HTTPException

from common.profile import ProfileCreate, ProfileRead, ProfileWithDistance
from common.enums import Gender

router = APIRouter(tags=["profiles"])


@router.get("/", response_model=list[ProfileRead])
async def get_profiles(
    session: db_dependency,
):
    profiles = await profiles_crud.get_all_profiles(session=session)
    return profiles


@router.post("/", response_model=ProfileRead)
async def create_profile(
    session: db_dependency,
    profile_create: ProfileCreate,
    # TODO in future:  user_id: UUID = Depends(get_user_id_from_JWT_token)
) -> ProfileRead:
    profile = await profiles_crud.create_profile(
        session=session,
        profile_create=profile_create,
    )
    return profile


@router.get("/{profile_id}", response_model=ProfileRead)
async def get_profile(
    session: db_dependency,
    profile_id: int,
) -> ProfileRead:
    profile = await profiles_crud.get_profile(
        session=session,
        profile_id=profile_id,
    )
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


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

    return matching_profiles
