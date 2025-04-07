from domain.models.preference import Preference
from domain.repositories.preference import IPreferenceRepository


class PreferenceService:
    def __init__(
        self,
        preference_repository: IPreferenceRepository,
    ):
        self.preference_repository = preference_repository

    async def get_preference_by_id(self, preference_id: int) -> Preference | None:
        return await self.preference_repository.get_preference_by_id(preference_id)

    async def get_preference_by_profile_id(self, profile_id: int) -> Preference | None:
        return await self.preference_repository.get_preference_by_profile_id(profile_id)

    async def get_preferences(self) -> list[Preference] | None:
        return await self.preference_repository.get_preferences()

    async def create_preference(self, preference: Preference) -> Preference | None:
        return await self.preference_repository.create_preference(preference)
