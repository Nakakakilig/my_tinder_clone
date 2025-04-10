from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from config.settings import settings
from domain.exceptions import (
    PreferenceForProfileNotFoundError,
    ProfileAlreadyExistsError,
    ProfileNotFoundError,
)
from domain.models.profile import Profile
from domain.repositories.profile import IProfileRepository
from infrastructure.db.db_models import ProfileORM
from infrastructure.mappers.profile import domain_to_orm, orm_to_domain
from utils.calc_distance import calc_distance_in_query


class ProfileRepositoryImpl(IProfileRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_profile_by_id(self, profile_id: int) -> Profile | None:
        stmt = select(ProfileORM).where(ProfileORM.outer_id == profile_id)
        result = await self.db_session.execute(stmt)
        profile_orm = result.scalar_one_or_none()
        if profile_orm is None:
            return None
        return orm_to_domain(profile_orm)

    async def create_profile(self, profile: Profile) -> Profile:
        existing_profile = await self.get_profile_by_id(profile.outer_id)
        if existing_profile:
            raise ProfileAlreadyExistsError(profile.outer_id)
        profile_orm = domain_to_orm(profile)
        self.db_session.add(profile_orm)
        await self.db_session.commit()
        await self.db_session.refresh(profile_orm)
        return orm_to_domain(profile_orm)

    async def get_profiles(self, limit: int, offset: int) -> list[Profile] | None:
        stmt = select(ProfileORM).order_by(ProfileORM.id).offset(offset).limit(limit)
        result = await self.db_session.execute(stmt)
        profiles_orm = result.scalars().all()
        if not profiles_orm:
            return None
        return [orm_to_domain(profile_orm) for profile_orm in profiles_orm]

    async def get_candidates_and_distance(
        self, profile_id: int, limit: int
    ) -> list[tuple[Profile, float]]:
        result = await self.db_session.execute(
            select(ProfileORM).where(ProfileORM.id == profile_id)
        )
        profile = result.scalars().first()

        if not profile:
            raise ProfileNotFoundError(profile_id)

        preference = profile.preference
        if not preference:
            raise PreferenceForProfileNotFoundError(profile_id)
        distance_expr = calc_distance_in_query(profile, ProfileORM)  # type: ignore

        filters = [
            ProfileORM.gender == preference.gender,
            ProfileORM.age >= preference.age - settings.deck.age_range,
            ProfileORM.age <= preference.age + settings.deck.age_range,
        ]
        query = (
            select(ProfileORM, distance_expr)
            .filter(and_(*filters))
            .group_by(ProfileORM.id)
            .order_by(distance_expr)
            .limit(limit)
        )

        query = query.having(distance_expr <= preference.radius)

        result = await self.db_session.execute(query)
        profiles_and_distance: list[tuple[ProfileORM, float]] = result.all()  # type: ignore
        return [(orm_to_domain(profile), distance) for profile, distance in profiles_and_distance]
