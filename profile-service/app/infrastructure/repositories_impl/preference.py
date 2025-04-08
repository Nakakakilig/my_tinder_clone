from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.preference import Preference
from domain.repositories.preference import IPreferenceRepository
from infrastructure.db.db_models import PreferenceORM
from infrastructure.mappers.preference import orm_to_domain


class PreferenceRepositoryImpl(IPreferenceRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_preference_by_id(self, preference_id: int) -> Preference | None:
        stmt = select(PreferenceORM).where(PreferenceORM.id == preference_id)
        result = await self.db_session.execute(stmt)
        preference_orm = result.scalar_one_or_none()
        if preference_orm is None:
            return None
        return orm_to_domain(preference_orm)

    async def get_preference_by_profile_id(self, profile_id: int) -> Preference | None:
        stmt = select(PreferenceORM).where(PreferenceORM.profile_id == profile_id)
        result = await self.db_session.execute(stmt)
        preference_orm = result.scalar_one_or_none()
        if preference_orm is None:
            return None
        return orm_to_domain(preference_orm)

    async def create_preference(self, preference: Preference) -> Preference:
        preference_orm = PreferenceORM(**preference.model_dump())
        self.db_session.add(preference_orm)
        await self.db_session.commit()
        await self.db_session.refresh(preference_orm)
        return orm_to_domain(preference_orm)

    async def get_preferences(self) -> list[Preference]:
        stmt = select(PreferenceORM).order_by(PreferenceORM.id)
        result = await self.db_session.execute(stmt)
        preference_orms = result.scalars().all()
        return [orm_to_domain(preference_orm) for preference_orm in preference_orms]
