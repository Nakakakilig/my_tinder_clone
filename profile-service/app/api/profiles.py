from api.deps import db_dependency
from crud import profiles as profiles_crud
from fastapi import APIRouter

from common.profile import ProfileCreate, ProfileRead

router = APIRouter(tags=["profiles"])


@router.get("/get-all", response_model=list[ProfileRead])
async def get_profiles(
    session: db_dependency,
):
    profiles = await profiles_crud.get_all_profiles(session=session)
    return profiles


@router.post("/create", response_model=ProfileRead)
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


@router.get("/get/{profile_id}", response_model=ProfileRead)
async def get_profile(
    session: db_dependency,
    profile_id: int,
) -> ProfileRead:
    profile = await profiles_crud.get_profile(
        session=session,
        profile_id=profile_id,
    )
    return profile
