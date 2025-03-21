from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.preference import Preference
from app.core.schemas.preferences import PreferenceCreate


async def create_preference(
    session: AsyncSession,
    preference_create: PreferenceCreate,
) -> Preference:
    preference = Preference(**preference_create.model_dump())
    session.add(preference)
    await session.commit()
    await session.refresh(preference)
    return preference


async def get_all_preferences(session: AsyncSession) -> Sequence[Preference]:
    stmt = select(Preference).order_by(Preference.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_preference(session: AsyncSession, preference_id: int) -> Preference:
    preference = await session.get(Preference, preference_id)
    return preference


async def get_preference_by_profile_id(
    session: AsyncSession, profile_id: int
) -> Preference:
    stmt = select(Preference).where(Preference.profile_id == profile_id)
    result = await session.scalars(stmt)
    return result.one_or_none()
