from abc import ABC, abstractmethod
from domain.models.profile import Profile


class IProfileRepository(ABC):
    @abstractmethod
    async def get_profile_by_id(self, profile_id: int) -> Profile | None:
        raise NotImplementedError

    @abstractmethod
    async def get_profiles(self) -> list[Profile]:
        raise NotImplementedError
