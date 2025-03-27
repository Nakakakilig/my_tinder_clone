from domain.models.profile import Profile
from domain.repositories.profile import IProfileRepository


class ProfileService:
    def __init__(
        self,
        profile_repository: IProfileRepository,
    ):
        self.profile_repository = profile_repository

    async def get_profile_by_id(self, profile_id: int) -> Profile:
        return await self.profile_repository.get_profile_by_id(profile_id)

    async def get_profiles(self) -> list[Profile]:
        return await self.profile_repository.get_profiles()

    async def create_profile(self, profile: Profile) -> Profile | None:
        return await self.profile_repository.create_profile(profile)
