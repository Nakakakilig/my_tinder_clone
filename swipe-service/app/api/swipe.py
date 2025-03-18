from fastapi import APIRouter

from app.api.deps import db_dependency

router = APIRouter(tags=["profiles"])


@router.post("/")
async def create_profile(
    session: db_dependency,
    who_like_id: int,
    liked_profile_id: int,
):
    raise NotImplementedError
