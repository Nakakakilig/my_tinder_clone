from typing import Annotated

from fastapi import APIRouter, Depends, Path

from domain.exceptions import ProfileNotFoundError
from presentation.dependencies.profile import get_profile_service
from presentation.mappers.profile import profile_to_read_schema, profiles_to_read_schema_list
from presentation.schemas.profile import ProfileReadSchema
from use_cases.profile import ProfileService

router = APIRouter(tags=["profiles"])


@router.get("/")
async def get_profiles(
    profile_service: Annotated[ProfileService, Depends(get_profile_service)],
) -> list[ProfileReadSchema]:
    profiles = await profile_service.get_profiles()
    if not profiles:
        raise ProfileNotFoundError()
    return profiles_to_read_schema_list(profiles)


@router.get("/{profile_id}")
async def get_profile(
    profile_id: Annotated[int, Path(gt=0)],
    profile_service: Annotated[ProfileService, Depends(get_profile_service)],
) -> ProfileReadSchema:
    profile = await profile_service.get_profile_by_id(profile_id)
    if not profile:
        raise ProfileNotFoundError(profile_id)
    return profile_to_read_schema(profile)
