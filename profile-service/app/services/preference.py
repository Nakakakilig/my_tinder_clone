from core.models.preference import Preference
from core.schemas.preferences import PreferenceCreate
from crud import preferences as crud_preference
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .kafka_producer import publish_preference_created_event


async def get_preferences_service(db: AsyncSession) -> list[Preference]:
    try:
        preferences = await crud_preference.get_all_preferences(db)
    except ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection refused. Please check if the DB is running.",
        )

    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preferences not found",
        )
    return preferences


async def create_preference_service(
    db: AsyncSession,
    preference_create: PreferenceCreate,
    need_event: bool = True,
) -> Preference:
    existing_preference = await crud_preference.get_preference(
        db, preference_create.profile_id
    )

    if existing_preference:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Preference already exists.",
        )

    preference = await crud_preference.create_preference(db, preference_create)
    if not preference:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Preference creation failed.",
        )

    if need_event:  # value false only for creating fake data
        # todo: add some handle for exceptions
        await publish_preference_created_event(preference_create)

    return preference


async def get_preference_service(db: AsyncSession, preference_id: int) -> Preference:
    preference = await crud_preference.get_preference(db, preference_id)
    if not preference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="preference not found",
        )
    return preference
