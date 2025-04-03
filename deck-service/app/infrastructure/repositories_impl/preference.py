from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.exceptions import (
    PreferenceAlreadyExistsError,
    PreferenceCreateError,
    PreferenceNotFoundError,
)
from domain.models.preference import Preference
from domain.repositories.preference import IPreferenceRepository
from infrastructure.db.db_models import PreferenceORM
from infrastructure.mappers.preference import domain_to_orm, orm_to_domain


class PreferenceRepositoryImpl(IPreferenceRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_preference(self, preference: Preference) -> Preference:
        try:
            existing_preference = await self.get_preference_by_profile_id(preference.profile_id)
            if existing_preference:
                raise PreferenceAlreadyExistsError(
                    f"Preference for profile {preference.profile_id} already exists"
                )
            preference_orm = domain_to_orm(preference)
            self.db_session.add(preference_orm)
            await self.db_session.commit()
            await self.db_session.refresh(preference_orm)
            return orm_to_domain(preference_orm)
        except Exception as e:
            raise PreferenceCreateError("Preference creation failed") from e

    async def get_preference_by_id(self, preference_id: int) -> Preference | None:
        try:
            stmt = select(PreferenceORM).where(PreferenceORM.id == preference_id)
            result = await self.db_session.execute(stmt)
            preference_orm = result.scalar_one_or_none()
            if preference_orm is None:
                return None
            return orm_to_domain(preference_orm)
        except Exception as e:
            raise PreferenceNotFoundError(f"Preference {preference_id} not found") from e

    async def get_preference_by_profile_id(self, profile_id: int) -> Preference | None:
        try:
            stmt = select(PreferenceORM).where(PreferenceORM.profile_id == profile_id)
            result = await self.db_session.execute(stmt)
            preference_orm = result.scalar_one_or_none()
            if preference_orm is None:
                return None
            return orm_to_domain(preference_orm)
        except Exception as e:
            raise PreferenceNotFoundError(f"Preference for profile {profile_id} not found") from e

    async def get_preferences(self) -> list[Preference] | None:
        try:
            stmt = select(PreferenceORM).order_by(PreferenceORM.id)
            result = await self.db_session.execute(stmt)
            preferences_orm = result.scalars().all()
            if not preferences_orm:
                return None
            return [orm_to_domain(preference_orm) for preference_orm in preferences_orm]
        except Exception as e:
            raise PreferenceNotFoundError("Preferences not found") from e
