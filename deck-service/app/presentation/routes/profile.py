from fastapi import APIRouter, Depends

from application.schemas.profile import ProfileRead
from application.services.profile import ProfileService
from presentation.dependencies.profile import get_profile_service

router = APIRouter(tags=["profiles"])


@router.get("/", response_model=list[ProfileRead])
async def get_profiles(
    profile_service: ProfileService = Depends(get_profile_service),
):
    return await profile_service.get_profiles()


@router.get("/{profile_id}", response_model=ProfileRead)
async def get_profile(
    profile_id: int,
    profile_service: ProfileService = Depends(get_profile_service),
) -> ProfileRead:
    return await profile_service.get_profile_by_id(profile_id)
