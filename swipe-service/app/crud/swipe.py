from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.swipe import Swipe
from app.core.schemas.swipe import SwipeCreate


async def get_all_swipes(session: AsyncSession) -> Sequence[Swipe]:
    stmt = select(Swipe).order_by(Swipe.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_swipe(
    session: AsyncSession,
    swipe_create: SwipeCreate,
) -> Swipe:
    swipe = Swipe(**swipe_create.model_dump())
    session.add(swipe)
    await session.commit()
    await session.refresh(swipe)
    return swipe


async def get_swipes_by_profile_id(
    session: AsyncSession, profile_id: int
) -> Sequence[Swipe]:
    """Get all swipes associated with a profile ID, either as profile_id_1 or profile_id_2."""
    stmt = select(Swipe).where(
        (Swipe.profile_id_1 == profile_id) | (Swipe.profile_id_2 == profile_id)
    )
    result = await session.scalars(stmt)
    return result.all()
