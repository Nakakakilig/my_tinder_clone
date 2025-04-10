from typing import Annotated

import logging
from fastapi import APIRouter, Depends, Path

from domain.exceptions import ProfileNotFoundError
from presentation.dependencies.profile import get_profile_service
from presentation.mappers.profile import profile_to_read_schema, profiles_to_read_schema_list
from presentation.routes.common import PaginationParams
from presentation.schemas.profile import ProfileReadSchema
from use_cases.profile import ProfileService

logger = logging.getLogger(__name__)
router = APIRouter(tags=["profiles"])


@router.get("/")
async def get_profiles(
    pagination: Annotated[PaginationParams, Depends()],
    profile_service: Annotated[ProfileService, Depends(get_profile_service)],
) -> list[ProfileReadSchema]:
    logger.info("Getting profiles")
    profiles = await profile_service.get_profiles(pagination.limit, pagination.offset)
    if not profiles:
        raise ProfileNotFoundError()
    profiles = profiles_to_read_schema_list(profiles)
    logger.info("Returning profiles")
    return profiles


@router.get("/{profile_id}")
async def get_profile(
    profile_id: Annotated[int, Path(gt=0)],
    profile_service: Annotated[ProfileService, Depends(get_profile_service)],
) -> ProfileReadSchema:
    logger.info("Getting profile by id: %d", profile_id)
    profile = await profile_service.get_profile_by_id(profile_id)
    if not profile:
        raise ProfileNotFoundError(profile_id)
    profile = profile_to_read_schema(profile)
    logger.info("Returning profile by id: %d", profile_id)
    return profile
