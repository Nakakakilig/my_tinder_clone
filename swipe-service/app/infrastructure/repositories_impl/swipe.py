from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.exceptions import SwipeCreateError
from domain.models.swipe import Swipe
from domain.repositories.swipe import ISwipeRepository
from infrastructure.db.db_models import SwipeORM
from infrastructure.mappers.swipe import domain_to_orm, orm_to_domain


class SwipeRepositoryImpl(ISwipeRepository):
    def __init__(
        self,
        db_session: AsyncSession,
    ):
        self.db_session = db_session

    async def create_swipe(self, swipe: Swipe) -> Swipe:
        swipe_orm = domain_to_orm(swipe)
        self.db_session.add(swipe_orm)
        await self.db_session.commit()
        await self.db_session.refresh(swipe_orm)
        return orm_to_domain(swipe_orm)

    async def get_swipes(self, limit: int, offset: int) -> list[Swipe] | None:
        try:
            stmt = (
                select(SwipeORM)
                .order_by(SwipeORM.id.desc())
                .limit(limit)
                .offset(offset)
            )
            result = await self.db_session.execute(stmt)
            swipes_orm = result.scalars().all()
            if not swipes_orm:
                return None
            return [orm_to_domain(swipe_orm) for swipe_orm in swipes_orm]
        except Exception as e:
            raise SwipeCreateError(
                "An error occurred while retrieving swipes"
            ) from e

    async def get_swipes_by_profile_id(
        self, profile_id: int, limit: int, offset: int
    ) -> list[Swipe] | None:
        stmt = (
            select(SwipeORM)
            .where(
                (SwipeORM.profile_id_1 == profile_id)
                | (SwipeORM.profile_id_2 == profile_id)
            )
            .order_by(SwipeORM.id.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.db_session.execute(stmt)
        swipes_orm = result.scalars().all()
        if not swipes_orm:
            return None
        return [orm_to_domain(swipe_orm) for swipe_orm in swipes_orm]

    async def get_swipe_by_two_profile_ids(
        self, profile_id_1: int, profile_id_2: int
    ) -> Swipe | None:
        stmt = select(SwipeORM).where(
            (
                (SwipeORM.profile_id_1 == profile_id_1)
                & (SwipeORM.profile_id_2 == profile_id_2)
            )
            | (
                (SwipeORM.profile_id_1 == profile_id_2)
                & (SwipeORM.profile_id_2 == profile_id_1)
            )
        )
        result = await self.db_session.execute(stmt)
        swipe_orm = result.scalar_one_or_none()
        if not swipe_orm:
            return None
        return orm_to_domain(swipe_orm)
