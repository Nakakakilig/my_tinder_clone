from typing import Annotated

import logging
from fastapi import APIRouter, Depends, Path

from domain.models.profile import Profile
from presentation.dependencies.profile import get_profile_service
from presentation.mappers.profile import profile_to_read_schema, profiles_to_read_schema_list
from presentation.routes.common import PaginationParams
from presentation.schemas.profile import ProfileCreateSchema, ProfileReadSchema
from use_cases.profile import ProfileService

logger = logging.getLogger(__name__)
router = APIRouter(tags=["profiles"])


@router.get("/")
async def get_profiles(
    profile_service: Annotated[ProfileService, Depends(get_profile_service)],
    pagination: Annotated[PaginationParams, Depends(PaginationParams)],
) -> list[ProfileReadSchema] | None:
    logger.info(
        "Incoming request: get_profiles (limit=%d, offset=%d)",
        pagination.limit,
        pagination.offset,
    )
    profiles = await profile_service.get_profiles(pagination.limit, pagination.offset)
    if not profiles:
        return None
    profiles = profiles_to_read_schema_list(profiles)
    logger.info("Returning profiles")
    return profiles


@router.post("/")
async def create_profile(
    profile_create: ProfileCreateSchema,
    profile_service: Annotated[ProfileService, Depends(get_profile_service)],
    # TODO in future:  user_id: UUID = Depends(get_user_id_from_JWT_token)
) -> ProfileReadSchema:
    logger.info("Incoming request: create_profile")
    profile_model = Profile(**profile_create.model_dump())
    profile = await profile_service.create_profile(profile_model)
    profile_read = profile_to_read_schema(profile)
    logger.info("Created profile with id %d", profile_read.id)
    return profile_read


@router.get("/{profile_id}")
async def get_profile(
    profile_id: Annotated[int, Path(gt=0)],
    profile_service: Annotated[ProfileService, Depends(get_profile_service)],
) -> ProfileReadSchema | None:
    logger.info("Incoming request: get_profile (profile_id=%d)", profile_id)
    profile = await profile_service.get_profile_by_id(profile_id)
    if not profile:
        return None
    profile_read = profile_to_read_schema(profile)
    logger.info("Returning profile with id %d", profile_read.id)
    return profile_read


@router.get("/user/{user_id}")
async def get_profile_by_user_id(
    user_id: Annotated[int, Path(gt=0)],
    profile_service: Annotated[ProfileService, Depends(get_profile_service)],
) -> ProfileReadSchema | None:
    logger.info("Incoming request: get_profile_by_user_id (user_id=%d)", user_id)
    profile = await profile_service.get_profile_by_user_id(user_id)
    if not profile:
        return None
    profile_read = profile_to_read_schema(profile)
    logger.info("Returning profile with id %d", profile_read.id)
    return profile_read
