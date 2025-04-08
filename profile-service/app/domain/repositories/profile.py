from abc import ABC, abstractmethod

from domain.models.profile import Profile


class IProfileRepository(ABC):
    @abstractmethod
    async def get_profile_by_id(self, profile_id: int) -> Profile | None:
        raise NotImplementedError

    @abstractmethod
    async def create_profile(self, profile: Profile) -> Profile:
        raise NotImplementedError

    @abstractmethod
    async def get_profile_by_user_id(self, user_id: int) -> Profile | None:
        raise NotImplementedError

    @abstractmethod
    async def get_profiles(self) -> list[Profile] | None:
        raise NotImplementedError
