from typing import Sequence

from core.models.profile import Profile
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from utils.calc_distance import calc_distance_in_query

from common.profile import ProfileCreate


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


async def get_profile(session: AsyncSession, profile_id: int) -> Profile:
    profile = await session.get(Profile, profile_id)
    return profile


async def get_matching_profiles(
    session: AsyncSession,
    profile_id: int | None,
    gender: str | None,
    age: int | None,
    radius: int | None,
    limit: int | None = 10,
) -> list[Profile]:
    current_profile = await session.get(Profile, profile_id)
    if not current_profile:
        return []

    distance_expr = calc_distance_in_query(current_profile, Profile)

    filters = [Profile.user_id != current_profile.user_id]
    if gender:
        filters.append(Profile.gender == gender)
    if age:
        filters.append(Profile.age >= age)

    query = (
        select(Profile, distance_expr)
        .filter(and_(*filters))
        .order_by(distance_expr)
        .limit(limit)
    )

    if radius:
        query = query.having(distance_expr <= radius)

    result = await session.execute(query)
    profiles: list[tuple[Profile, float]] = result.all()

    matching_profiles = [
        {"profile": profile.__dict__, "distance_km": float(distance)}
        for profile, distance in profiles
    ]

    return matching_profiles
