from abc import ABC, abstractmethod
from domain.models.preference import Preference


class IPreferenceRepository(ABC):
    @abstractmethod
    async def get_preference_by_id(self, preference_id: int) -> Preference | None:
        raise NotImplementedError

    @abstractmethod
    async def create_preference(self, preference: Preference) -> Preference:
        raise NotImplementedError

    @abstractmethod
    async def get_preference_by_profile_id(self, profile_id: int) -> Preference | None:
        raise NotImplementedError

    @abstractmethod
    async def get_preferences(self) -> list[Preference]:
        raise NotImplementedError
