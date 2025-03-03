from typing import Sequence

from core.models.profile import Profile
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

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
) -> list[Profile]:
    current_profile = await session.get(Profile, profile_id)
    if not current_profile:
        return []

    filters = [Profile.user_id != current_profile.user_id]
    if gender:
        filters.append(Profile.gender == gender)
    if age:
        filters.append(Profile.age >= age)
    if radius:
        pass

    query = select(Profile).where(and_(*filters))
    result = await session.execute(query)
    profiles = result.scalars().all()

    if not profiles:
        return []
    if not radius:
        return profiles

    matching_profiles: list[Profile] = []
    for profile in profiles:
        distance = calculate_distance(
            current_profile.geo_latitude,
            current_profile.geo_longitude,
            profile.geo_latitude,
            profile.geo_longitude,
        )
        if distance <= radius:
            matching_profiles.append(profile)

    return matching_profiles


def calculate_distance(lat1, lon1, lat2, lon2):
    from math import radians, sin, cos, sqrt, atan2

    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c
