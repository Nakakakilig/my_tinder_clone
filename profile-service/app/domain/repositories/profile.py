from abc import ABC, abstractmethod


class IProfileRepository(ABC):
    @abstractmethod
    async def get_profile_by_id(self):
        raise NotImplementedError

    @abstractmethod
    async def create_profile(self):
        raise NotImplementedError

    @abstractmethod
    async def get_profile_by_user_id(self):
        raise NotImplementedError

    @abstractmethod
    async def get_profiles(self):
        raise NotImplementedError
