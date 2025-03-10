from core.schemas.profile import ProfileRead
from crud import profile as profiles_crud
from fastapi import APIRouter

from api.deps import db_dependency

router = APIRouter(tags=["profiles"])


@router.get("/", response_model=list[ProfileRead])
async def get_profiles(
    session: db_dependency,
):
    return await profiles_crud.get_all_profiles(session)


@router.get("/{profile_id}", response_model=ProfileRead)
async def get_profile(
    session: db_dependency,
    profile_id: int,
) -> ProfileRead:
    return await profiles_crud.get_profile(session, profile_id)
