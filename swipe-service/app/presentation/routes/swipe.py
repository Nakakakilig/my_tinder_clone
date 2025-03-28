from fastapi import APIRouter, Depends, Query

from application.schemas.swipe import SwipeCreateSchema, SwipeReadSchema
from application.services.swipe import SwipeService
from presentation.dependencies.swipe import get_swipe_service

router = APIRouter(tags=["swipes"])


@router.get("/")
async def get_swipes(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    swipe_service: SwipeService = Depends(get_swipe_service),
) -> list[SwipeReadSchema]:
    return await swipe_service.get_swipes(limit, offset)


@router.post("/")
async def create_swipe(
    swipe: SwipeCreateSchema,
    swipe_service: SwipeService = Depends(get_swipe_service),
) -> SwipeReadSchema:
    return await swipe_service.create_swipe(swipe)


@router.get("/profile/{profile_id}/")
async def get_swipes_by_profile_id(
    profile_id: int,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    swipe_service: SwipeService = Depends(get_swipe_service),
) -> list[SwipeReadSchema]:
    """Get all swipes associated with a profile ID."""
    return await swipe_service.get_swipes_by_profile_id(profile_id, limit, offset)
