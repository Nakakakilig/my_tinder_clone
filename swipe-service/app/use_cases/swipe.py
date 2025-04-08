from domain.models.swipe import Swipe
from domain.repositories.swipe import ISwipeRepository


class SwipeService:
    def __init__(
        self,
        swipe_repository: ISwipeRepository,
    ):
        self.swipe_repository = swipe_repository

    async def create_swipe(self, swipe: Swipe) -> Swipe:
        swipe = await self.swipe_repository.create_swipe(swipe)
        return swipe

    async def get_swipes(self, limit: int, offset: int) -> list[Swipe] | None:
        return await self.swipe_repository.get_swipes(limit, offset)

    async def get_swipes_by_profile_id(
        self, profile_id: int, limit: int, offset: int
    ) -> list[Swipe] | None:
        return await self.swipe_repository.get_swipes_by_profile_id(profile_id, limit, offset)

    async def get_swipe_by_two_profile_ids(
        self, profile_id_1: int, profile_id_2: int
    ) -> Swipe | None:
        swipe = await self.swipe_repository.get_swipe_by_two_profile_ids(profile_id_1, profile_id_2)
        return swipe
