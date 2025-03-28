from abc import ABC, abstractmethod


class ISwipeRepository(ABC):
    @abstractmethod
    async def create_swipe(self):
        raise NotImplementedError

    @abstractmethod
    async def get_swipes(self):
        raise NotImplementedError

    @abstractmethod
    async def get_swipes_by_profile_id(self):
        raise NotImplementedError

    @abstractmethod
    async def get_swipe_by_two_profile_ids(self):
        raise NotImplementedError
