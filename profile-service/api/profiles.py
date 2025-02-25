from core.schemas.profile import ProfileCreate, ProfileRead
from fastapi import APIRouter
from api.deps import db_dependency
from crud import profiles as profiles_crud

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
