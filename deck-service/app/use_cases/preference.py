import logging

from domain.models.preference import Preference
from domain.repositories.preference import IPreferenceRepository

logger = logging.getLogger(__name__)


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

    async def get_preferences(self, limit: int, offset: int) -> list[Preference] | None:
        return await self.preference_repository.get_preferences(limit, offset)

    async def create_preference(self, preference: Preference) -> Preference | None:
        logger.info("Creating preference for profile: %s", preference.profile_id)
        preference = await self.preference_repository.create_preference(preference)
        logger.info("Preference created for profile: %s", preference.profile_id)
        return preference
