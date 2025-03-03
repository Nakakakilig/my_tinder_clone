from typing import Sequence

from core.models.preference import Preference
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.preferences import PreferenceCreate


async def get_all_profiles(session: AsyncSession) -> Sequence[Preference]:
    stmt = select(Preference).order_by(Preference.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_profile(
    session: AsyncSession,
    preference_create: PreferenceCreate,
) -> Preference:
    preference = Preference(**preference_create.model_dump())
    session.add(preference)
    await session.commit()
    await session.refresh(preference)
    return preference


async def get_profile(session: AsyncSession, preference_id: int) -> Preference:
    profile = await session.get(Preference, preference_id)
    return profile
