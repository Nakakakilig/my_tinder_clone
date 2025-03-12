from app.core.models.profile import Profile
from app.core.schemas.profile import ProfileCreate
from app.crud import profile as crud_profile
from app.exceptions.profiles import (
    ProfileAlreadyExists,
    ProfileCreationFailed,
    ProfileNotFound,
)
from sqlalchemy.ext.asyncio import AsyncSession


async def get_profiles_service(db: AsyncSession) -> list[Profile]:
    try:
        profiles = await crud_profile.get_all_profiles(db)
    except ConnectionError:
        raise ConnectionError()

    if not profiles:
        raise ProfileNotFound()

    return profiles


async def create_profile_service(
    db: AsyncSession,
    profile_create: ProfileCreate,
) -> Profile:
    existing_profile = await crud_profile.get_profile_by_outer_id(
        db, profile_create.outer_id
    )
    if existing_profile:
        raise ProfileAlreadyExists()

    profile = await crud_profile.create_profile(db, profile_create)
    if not profile:
        raise ProfileCreationFailed()

    return profile


async def get_profile_service(db: AsyncSession, profile_id: int) -> Profile:
    profile = await crud_profile.get_profile_by_outer_id(db, profile_id)
    if not profile:
        raise ProfileNotFound()

    return profile
