from typing import Sequence

from core.models.profile import Profile
from core.schemas.profile import ProfileCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_profiles(session: AsyncSession) -> Sequence[Profile]:
    stmt = select(Profile).order_by(Profile.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_profile(
    session: AsyncSession,
    profile_create: ProfileCreate,
) -> Profile:
    profile = Profile(**profile_create.model_dump())
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile
