from abc import ABC, abstractmethod


class IPreferenceRepository(ABC):
    @abstractmethod
    async def get_preference_by_id(self):
        raise NotImplementedError

    @abstractmethod
    async def get_preference_by_profile_id(self):
        raise NotImplementedError

    @abstractmethod
    async def get_preferences(self):
        raise NotImplementedError

    @abstractmethod
    async def create_preference(self):
        raise NotImplementedError
