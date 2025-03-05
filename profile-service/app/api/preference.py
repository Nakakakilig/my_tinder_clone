from api.deps import db_dependency
from crud import preferences as preferences_crud
from fastapi import APIRouter

from common.preferences import PreferenceCreate, PreferenceRead

router = APIRouter(tags=["preferences"])


@router.get("/get-all", response_model=list[PreferenceRead])
async def get_profiles(
    session: db_dependency,
):
    profiles = await preferences_crud.get_all_profiles(session=session)
    return profiles


@router.post("/create", response_model=PreferenceRead)
async def create_profile(
    session: db_dependency,
    profile_create: PreferenceCreate,
    # TODO in future:  user_id: UUID = Depends(get_user_id_from_JWT_token)
) -> PreferenceRead:
    profile = await preferences_crud.create_profile(
        session=session,
        profile_create=profile_create,
    )
    return profile


@router.get("/{preference_id}", response_model=PreferenceRead)
async def get_profile(
    session: db_dependency,
    preference_id: int,
) -> PreferenceRead:
    profile = await preferences_crud.get_profile(
        session=session,
        preference_id=preference_id,
    )
    return profile
