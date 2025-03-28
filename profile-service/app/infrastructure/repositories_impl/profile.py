from application.schemas.profile import ProfileCreateSchema
from domain.repositories.profile import IProfileRepository
from infrastructure.db.db_models import ProfileORM
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ProfileRepositoryImpl(IProfileRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_profile_by_id(self, profile_id: int) -> ProfileORM | None:
        stmt = select(ProfileORM).where(ProfileORM.id == profile_id)
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_profile_by_user_id(self, user_id: int) -> ProfileORM | None:
        stmt = select(ProfileORM).where(ProfileORM.user_id == user_id)
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_profile(self, profile: ProfileCreateSchema) -> ProfileORM:
        profile_orm = ProfileORM(**profile.model_dump())
        self.db_session.add(profile_orm)
        await self.db_session.commit()
        await self.db_session.refresh(profile_orm)
        return profile_orm

    async def get_profiles(self) -> list[ProfileORM]:
        stmt = select(ProfileORM).order_by(ProfileORM.id)
        result = await self.db_session.execute(stmt)
        return result.scalars().all()
