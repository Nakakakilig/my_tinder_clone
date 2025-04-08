from typing import Annotated

from fastapi import APIRouter, Depends

from domain.models.profile import Profile
from presentation.dependencies.profile import get_profile_service
from presentation.mappers.profile import profile_to_read_schema, profiles_to_read_schema_list
from presentation.routes.common import PaginationParams
from presentation.schemas.profile import ProfileCreateSchema, ProfileReadSchema
from use_cases.profile import ProfileService

router = APIRouter(tags=["profiles"])


@router.get("/")
async def get_profiles(
    profile_service: Annotated[ProfileService, Depends(get_profile_service)],
    pagination: Annotated[PaginationParams, Depends(PaginationParams)],
) -> list[ProfileReadSchema] | None:
    profiles = await profile_service.get_profiles(pagination.limit, pagination.offset)
    if not profiles:
        return None
    return profiles_to_read_schema_list(profiles)


@router.post("/")
async def create_profile(
    profile_create: ProfileCreateSchema,
    profile_service: Annotated[ProfileService, Depends(get_profile_service)],
    # TODO in future:  user_id: UUID = Depends(get_user_id_from_JWT_token)
) -> ProfileReadSchema:
    profile_model = Profile(**profile_create.model_dump())
    profile = await profile_service.create_profile(profile_model)
    return profile_to_read_schema(profile)


@router.get("/{profile_id}")
async def get_profile(
    profile_id: int,
    profile_service: Annotated[ProfileService, Depends(get_profile_service)],
) -> ProfileReadSchema | None:
    profile = await profile_service.get_profile_by_id(profile_id)
    if not profile:
        return None
    return profile_to_read_schema(profile)


@router.get("/user/{user_id}")
async def get_profile_by_user_id(
    user_id: int,
    profile_service: Annotated[ProfileService, Depends(get_profile_service)],
) -> ProfileReadSchema | None:
    profile = await profile_service.get_profile_by_user_id(user_id)
    if not profile:
        return None
    return profile_to_read_schema(profile)
