from abc import ABC, abstractmethod

from domain.models.profile import Profile


class IProfileRepository(ABC):
    @abstractmethod
    async def get_profile_by_id(self, profile_id: int) -> Profile | None:
        raise NotImplementedError

    @abstractmethod
    async def get_profiles(self, limit: int, offset: int) -> list[Profile] | None:
        raise NotImplementedError

    @abstractmethod
    async def create_profile(self, profile: Profile) -> Profile:
        raise NotImplementedError

    @abstractmethod
    async def get_candidates_and_distance(
        self, profile_id: int, limit: int
    ) -> list[tuple[Profile, float]] | None:
        raise NotImplementedError
