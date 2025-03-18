from typing import Sequence

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.profile import Profile
from app.core.schemas.profile import ProfileCreate
from app.core.schemas.preferences import PreferenceBase
from app.utils.calc_distance import calc_distance_in_query


async def create_profile(
    session: AsyncSession,
    profile_create: ProfileCreate,
) -> Profile:
    profile = Profile(**profile_create.model_dump())
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile


async def get_all_profiles(session: AsyncSession) -> Sequence[Profile]:
    stmt = select(Profile).order_by(Profile.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_profile_by_outer_id(session: AsyncSession, outer_id: int) -> Profile:
    stmt = select(Profile).where(Profile.outer_id == outer_id)
    result = await session.scalars(stmt)
    return result.one_or_none()


async def get_matching_profiles(
    session: AsyncSession,
    profile_id: int,
    preferences: PreferenceBase,
    limit: int,
):
    current_profile = await session.get(Profile, profile_id)
    if not current_profile:
        return None

    distance_expr = calc_distance_in_query(current_profile, Profile)

    filters = [
        Profile.id != current_profile.id,
        Profile.gender == preferences.gender,
        Profile.age >= preferences.age - 5,
        Profile.age <= preferences.age + 5,
    ]

    query = (
        select(Profile, distance_expr)
        .filter(and_(*filters))
        .group_by(Profile.id)
        .order_by(distance_expr)
        .limit(limit)
    )

    query = query.having(distance_expr <= preferences.radius)

    result = await session.execute(query)
    profiles: list[tuple[Profile, float]] = result.all()

    matching_profiles = [
        {"profile": profile.__dict__, "distance_km": float(distance)}
        for profile, distance in profiles
    ]

    return matching_profiles
