from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.profile import Profile
from app.core.schemas.profile import ProfileCreate


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


async def get_profile_by_user_id(session: AsyncSession, user_id: int) -> Profile:
    stmt = select(Profile).where(Profile.user_id == user_id)
    result = await session.scalars(stmt)
    return result.one_or_none()
