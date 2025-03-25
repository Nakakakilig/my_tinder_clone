from fastapi import APIRouter

from presentation.dependencies.db_session import db_dependency
from application.schemas.profile import ProfileRead

router = APIRouter(tags=["profiles"])


@router.get("/")  # , response_model=list[ProfileRead])
async def get_profiles(
    session: db_dependency,
):
    return {"message": "Get all profiles"}
    # return await profiles_crud.get_all_profiles(session)


@router.get("/{profile_id}")  # , response_model=ProfileRead)
async def get_profile(
    session: db_dependency,
    profile_id: int,
) -> ProfileRead:
    return {"message": f"Get profile {profile_id}"}
    # return await profiles_crud.get_profile(session, profile_id)
