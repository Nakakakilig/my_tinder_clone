from domain.models.preference import Preference
from domain.repositories.preference import IPreferenceRepository
from infrastructure.db.db_models import PreferenceORM
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class PreferenceRepositoryImpl(IPreferenceRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_preference_by_id(self, preference_id: int) -> PreferenceORM | None:
        stmt = select(PreferenceORM).where(PreferenceORM.id == preference_id)
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_preference_by_profile_id(
        self, profile_id: int
    ) -> PreferenceORM | None:
        stmt = select(PreferenceORM).where(PreferenceORM.profile_id == profile_id)
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_preference(self, preference: Preference) -> PreferenceORM:
        preference_orm = PreferenceORM(**preference.model_dump())
        self.db_session.add(preference_orm)
        await self.db_session.commit()
        await self.db_session.refresh(preference_orm)
        return preference_orm

    async def get_preferences(self) -> list[PreferenceORM]:
        stmt = select(PreferenceORM).order_by(PreferenceORM.id)
        result = await self.db_session.execute(stmt)
        return result.scalars().all()
