from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Swipe:
    profile_id_1: int
    profile_id_2: int
    decision_1: bool | None
    decision_2: bool | None


class ISwipeRepository(ABC):
    @abstractmethod
    async def get_swipes_for_profile(self, profile_id: int) -> list[Swipe] | None:
        raise NotImplementedError

    async def get_swipe_by_two_profile_ids(
        self, profile_id_1: int, profile_id_2: int
    ) -> Swipe | None:
        raise NotImplementedError
