from abc import ABC, abstractmethod

from domain.models.swipe import Swipe


class ISwipeRepository(ABC):
    @abstractmethod
    async def create_swipe(self, swipe: Swipe) -> Swipe:
        raise NotImplementedError

    @abstractmethod
    async def get_swipes(self, limit: int, offset: int) -> list[Swipe] | None:
        raise NotImplementedError

    @abstractmethod
    async def get_swipes_by_profile_id(
        self, profile_id: int, limit: int, offset: int
    ) -> list[Swipe] | None:
        raise NotImplementedError

    @abstractmethod
    async def get_swipe_by_two_profile_ids(
        self, profile_id_1: int, profile_id_2: int
    ) -> Swipe | None:
        raise NotImplementedError
