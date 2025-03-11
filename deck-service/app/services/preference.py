from core.models.preference import Preference
from core.schemas.preferences import PreferenceCreate
from crud import preference as crud_preference
from exceptions.preferences import (
    PreferenceAlreadyExists,
    PreferenceCreationFailed,
    PreferenceNotFound,
)
from sqlalchemy.ext.asyncio import AsyncSession


async def get_preferences_service(db: AsyncSession) -> list[Preference]:
    try:
        preferences = await crud_preference.get_all_preferences(db)
    except ConnectionError:
        raise ConnectionError()

    if not preferences:
        raise PreferenceNotFound()

    return preferences


async def create_preference_service(
    db: AsyncSession,
    preference_create: PreferenceCreate,
) -> Preference:
    existing_preference = await crud_preference.get_preference(
        db, preference_create.profile_id
    )
    if existing_preference:
        raise PreferenceAlreadyExists()

    preference = await crud_preference.create_preference(db, preference_create)
    if not preference:
        raise PreferenceCreationFailed()

    return preference


async def get_preference_service(db: AsyncSession, preference_id: int) -> Preference:
    preference = await crud_preference.get_preference(db, preference_id)
    if not preference:
        raise PreferenceNotFound()
    return preference
