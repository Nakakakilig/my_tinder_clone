from typing import Annotated

import logging
from fastapi import APIRouter, Depends, Path, Query
from pydantic import BaseModel

from config.settings import settings
from domain.models.swipe import Swipe
from presentation.dependencies.swipe import get_swipe_service
from presentation.mappers.swipe import (
    swipe_to_read_schema,
    swipes_to_read_schema_list,
)
from presentation.schemas.swipe import SwipeCreateSchema, SwipeReadSchema
from use_cases.swipe import SwipeService

router = APIRouter(tags=["swipes"])
logger = logging.getLogger(__name__)


class PaginationParams(BaseModel):
    limit: int = Query(
        default=settings.pagination.default_limit,
        ge=settings.pagination.min_limit,
        le=settings.pagination.max_limit,
    )
    offset: int = Query(
        default=settings.pagination.default_offset,
        ge=settings.pagination.min_offset,
        le=settings.pagination.max_offset,
    )


@router.get("/")
async def get_swipes(
    swipe_service: Annotated[SwipeService, Depends(get_swipe_service)],
    pagination: Annotated[PaginationParams, Depends(PaginationParams)],
) -> list[SwipeReadSchema] | None:
    logger.info(
        "Incoming request: get_swipes (limit=%d, offset=%d)",
        pagination.limit,
        pagination.offset,
    )
    swipes = await swipe_service.get_swipes(pagination.limit, pagination.offset)
    if not swipes:
        return None
    swipes = swipes_to_read_schema_list(swipes)
    logger.info("Returning swipes")
    return swipes


@router.post("/")
async def create_swipe(
    swipe: SwipeCreateSchema,
    swipe_service: Annotated[SwipeService, Depends(get_swipe_service)],
) -> SwipeReadSchema:
    logger.info("Incoming request: create_swipe")
    swipe_model = Swipe(**swipe.model_dump())
    created_swipe = await swipe_service.create_swipe(swipe_model)
    swipe_read = swipe_to_read_schema(created_swipe)
    logger.info(
        "Created swipe for profile_id %d and profile_id %d",
        swipe_read.profile_id_1,
        swipe_read.profile_id_2,
    )
    return swipe_read


@router.get("/profile/{profile_id}/")
async def get_swipes_by_profile_id(
    profile_id: Annotated[int, Path(gt=0)],
    swipe_service: Annotated[SwipeService, Depends(get_swipe_service)],
    pagination: Annotated[PaginationParams, Depends(PaginationParams)],
) -> list[SwipeReadSchema] | None:
    """Get all swipes associated with a profile ID."""
    logger.info("Incoming request: get_swipes_by_profile_id (profile_id=%d)", profile_id)
    swipes = await swipe_service.get_swipes_by_profile_id(
        profile_id, pagination.limit, pagination.offset
    )
    if not swipes:
        return None
    swipes = swipes_to_read_schema_list(swipes)
    logger.info("Returning swipes for profile_id %d", profile_id)
    return swipes


@router.get("/profile/{profile_id_1}/profile/{profile_id_2}/")
async def get_swipe_by_two_profile_ids(
    profile_id_1: Annotated[int, Path(gt=0)],
    profile_id_2: Annotated[int, Path(gt=0)],
    swipe_service: Annotated[SwipeService, Depends(get_swipe_service)],
) -> SwipeReadSchema | None:
    logger.info(f"get_swipe_by_two_profile_ids: {profile_id_1}, {profile_id_2}")
    swipe = await swipe_service.get_swipe_by_two_profile_ids(profile_id_1, profile_id_2)
    if not swipe:
        return None
    swipe = swipe_to_read_schema(swipe)
    logger.info("Returning swipe for profile_id %d", profile_id_1)
    return swipe
