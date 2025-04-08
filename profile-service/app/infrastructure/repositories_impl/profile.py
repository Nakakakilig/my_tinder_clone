from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.profile import Profile
from domain.repositories.profile import IProfileRepository
from infrastructure.db.db_models import ProfileORM
from infrastructure.mappers.profile import domain_to_orm, orm_to_domain


class ProfileRepositoryImpl(IProfileRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_profile_by_id(self, profile_id: int) -> Profile | None:
        stmt = select(ProfileORM).where(ProfileORM.id == profile_id)
        result = await self.db_session.execute(stmt)
        profile_orm = result.scalar_one_or_none()
        if profile_orm is None:
            return None
        return orm_to_domain(profile_orm)

    async def get_profile_by_user_id(self, user_id: int) -> Profile | None:
        stmt = select(ProfileORM).where(ProfileORM.user_id == user_id)
        result = await self.db_session.execute(stmt)
        profile_orm = result.scalar_one_or_none()
        if profile_orm is None:
            return None
        return orm_to_domain(profile_orm)

    async def create_profile(self, profile: Profile) -> Profile:
        profile_orm = domain_to_orm(profile)
        self.db_session.add(profile_orm)
        await self.db_session.commit()
        await self.db_session.refresh(profile_orm)
        return orm_to_domain(profile_orm)

    async def get_profiles(self) -> list[Profile] | None:
        stmt = select(ProfileORM).order_by(ProfileORM.id)
        result = await self.db_session.execute(stmt)
        profiles_orm = result.scalars().all()
        if not profiles_orm:
            return None
        return [orm_to_domain(profile_orm) for profile_orm in profiles_orm]
