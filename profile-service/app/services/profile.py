from core.models.profile import Profile
from core.schemas.profile import ProfileCreate
from crud import profiles as crud_profile
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .kafka_producer import publish_profile_created_event


async def get_profiles_service(db: AsyncSession) -> list[Profile]:
    try:
        profiles = await crud_profile.get_all_profiles(db)
    except ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection refused. Please check if the DB is running.",
        )

    if not profiles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profiles not found",
        )
    return profiles


async def create_profile_service(
    db: AsyncSession,
    profile_create: ProfileCreate,
    need_event: bool = True,
) -> Profile:
    existing_profile = await crud_profile.get_profile(db, profile_create.user_id)

    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists.",
        )

    profile = await crud_profile.create_profile(db, profile_create)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Profile creation failed.",
        )

    if need_event:  # value false only for creating fake data
        # todo: add some handle for exceptions
        await publish_profile_created_event(profile_create)

    return profile


async def get_profile_service(db: AsyncSession, profile_id: int) -> Profile:
    profile = await crud_profile.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    return profile
