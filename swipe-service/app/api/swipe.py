from fastapi import APIRouter

from app.api.deps import db_dependency
from app.core.schemas.swipe import SwipeCreate
import app.crud.swipe as swipe_crud

router = APIRouter(tags=["swipes"])


@router.get("/")
async def get_swipes(
    session: db_dependency,
):
    return await swipe_crud.get_all_swipes(session)


@router.post("/")
async def create_swipe(
    session: db_dependency,
    swipe_create: SwipeCreate,
):
    return await swipe_crud.create_swipe(session, swipe_create)


@router.get("/profile/{profile_id}/swipes")
async def get_swipes_by_profile_id(
    session: db_dependency,
    profile_id: int,
):
    """Get all swipes associated with a profile ID."""
    return await swipe_crud.get_swipes_by_profile_id(session, profile_id)
