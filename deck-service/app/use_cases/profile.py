import logging

from domain.models.profile import Profile
from domain.repositories.profile import IProfileRepository

logger = logging.getLogger(__name__)


class ProfileService:
    def __init__(
        self,
        profile_repository: IProfileRepository,
    ):
        self.profile_repository = profile_repository

    async def get_profile_by_id(self, profile_id: int) -> Profile | None:
        return await self.profile_repository.get_profile_by_id(profile_id)

    async def get_profiles(self, limit: int, offset: int) -> list[Profile] | None:
        return await self.profile_repository.get_profiles(limit, offset)

    async def create_profile(self, profile: Profile) -> Profile | None:
        logger.info("Creating profile: %s", profile.id)
        profile = await self.profile_repository.create_profile(profile)
        logger.info("Profile created: %s", profile.id)
        return profile
