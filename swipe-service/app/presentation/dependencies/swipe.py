from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.services.swipe import SwipeService
from infrastructure.repositories_impl.swipe import SwipeRepositoryImpl
from presentation.dependencies.db_session import get_db_session


def get_swipe_service(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> SwipeService:
    swipe_repository = SwipeRepositoryImpl(db_session)
    return SwipeService(swipe_repository)
