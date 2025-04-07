from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel, ValidationError

from application.schemas.swipe import SwipeCreateSchema, SwipeReadSchema
from application.services.swipe import SwipeService
from config.settings import settings
from domain.exceptions import SwipeCreateError
from domain.models.swipe import Swipe
from presentation.dependencies.swipe import get_swipe_service
from presentation.mappers.swipe import (
    swipe_to_read_schema,
    swipes_to_read_schema_list,
)

router = APIRouter(tags=["swipes"])


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
    try:
        swipes = await swipe_service.get_swipes(pagination.limit, pagination.offset)
        if not swipes:
            return None
        return swipes_to_read_schema_list(swipes)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid input or output data",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        ) from e


@router.post("/")
async def create_swipe(
    swipe: SwipeCreateSchema,
    swipe_service: Annotated[SwipeService, Depends(get_swipe_service)],
) -> SwipeReadSchema:
    try:
        swipe_model = Swipe(**swipe.model_dump())
        created_swipe: Swipe | None = await swipe_service.create_swipe(swipe_model)
        if created_swipe:
            return swipe_to_read_schema(created_swipe)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Swipe not created",
        )
    except (ValidationError, SwipeCreateError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid input or output data",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        ) from e


@router.get("/profile/{profile_id}/")
async def get_swipes_by_profile_id(
    profile_id: Annotated[int, Path(gt=0)],
    swipe_service: Annotated[SwipeService, Depends(get_swipe_service)],
    pagination: Annotated[PaginationParams, Depends(PaginationParams)],
) -> list[SwipeReadSchema] | None:
    """Get all swipes associated with a profile ID."""
    try:
        swipes = await swipe_service.get_swipes_by_profile_id(
            profile_id, pagination.limit, pagination.offset
        )
        if not swipes:
            return None
        return swipes_to_read_schema_list(swipes)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        ) from e


@router.get("/profile/{profile_id_1}/profile/{profile_id_2}/")
async def get_swipe_by_two_profile_ids(
    profile_id_1: Annotated[int, Path(gt=0)],
    profile_id_2: Annotated[int, Path(gt=0)],
    swipe_service: Annotated[SwipeService, Depends(get_swipe_service)],
) -> SwipeReadSchema | None:
    try:
        swipe = await swipe_service.get_swipe_by_two_profile_ids(profile_id_1, profile_id_2)
        if not swipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No swipe found for \
                    profile {profile_id_1} and profile {profile_id_2}",
            )
        return swipe_to_read_schema(swipe)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        ) from e
