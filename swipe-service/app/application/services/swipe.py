from application.schemas.swipe import SwipeCreateSchema, SwipeReadSchema
from domain.repositories.swipe import ISwipeRepository


class SwipeService:
    def __init__(
        self,
        swipe_repository: ISwipeRepository,
    ):
        self.swipe_repository = swipe_repository

    async def create_swipe(self, swipe: SwipeCreateSchema) -> SwipeReadSchema:
        swipe = await self.swipe_repository.create_swipe(swipe)
        return SwipeReadSchema.model_validate(swipe)

    async def get_swipes(self, limit: int, offset: int) -> list[SwipeReadSchema] | None:
        return await self.swipe_repository.get_swipes(limit, offset)

    async def get_swipes_by_profile_id(
        self, profile_id: int, limit: int, offset: int
    ) -> list[SwipeReadSchema] | None:
        return await self.swipe_repository.get_swipes_by_profile_id(
            profile_id, limit, offset
        )

    async def get_swipe_by_two_profile_ids(
        self, profile_id_1: int, profile_id_2: int
    ) -> SwipeReadSchema | None:
        swipe = await self.swipe_repository.get_swipe_by_two_profile_ids(
            profile_id_1, profile_id_2
        )
        return SwipeReadSchema.model_validate(swipe) if swipe else None
