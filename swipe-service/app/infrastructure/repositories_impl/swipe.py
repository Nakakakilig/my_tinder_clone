from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.schemas.swipe import SwipeCreateSchema
from domain.repositories.swipe import ISwipeRepository
from infrastructure.db.db_models import SwipeORM


class SwipeRepositoryImpl(ISwipeRepository):
    def __init__(
        self,
        db_session: AsyncSession,
    ):
        self.db_session = db_session

    async def create_swipe(self, swipe: SwipeCreateSchema) -> SwipeORM:
        swipe_orm = SwipeORM(**swipe.model_dump())
        self.db_session.add(swipe_orm)
        await self.db_session.commit()
        await self.db_session.refresh(swipe_orm)
        return swipe_orm

    async def get_swipes(self, limit: int, offset: int) -> list[SwipeORM] | None:
        stmt = select(SwipeORM).order_by(SwipeORM.id.desc()).limit(limit).offset(offset)
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def get_swipes_by_profile_id(
        self, profile_id: int, limit: int, offset: int
    ) -> list[SwipeORM] | None:
        stmt = (
            select(SwipeORM)
            .where((SwipeORM.profile_id_1 == profile_id) | (SwipeORM.profile_id_2 == profile_id))
            .order_by(SwipeORM.id.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def get_swipe_by_two_profile_ids(
        self, profile_id_1: int, profile_id_2: int
    ) -> SwipeORM | None:
        stmt = select(SwipeORM).where(
            ((SwipeORM.profile_id_1 == profile_id_1) & (SwipeORM.profile_id_2 == profile_id_2))
            | ((SwipeORM.profile_id_1 == profile_id_2) & (SwipeORM.profile_id_2 == profile_id_1))
        )
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()
