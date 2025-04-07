from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.services.deck import DeckService
from config.settings import settings
from domain.repositories.cache import ICache
from infrastructure.repositories_impl.deck import DeckRepositoryImpl
from infrastructure.repositories_impl.profile import ProfileRepositoryImpl
from infrastructure.swipe_client.swipe import SwipeClient
from presentation.dependencies.cache import get_cache
from presentation.dependencies.db_session import get_db_session


def get_deck_service(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    cache: Annotated[ICache, Depends(get_cache)],
) -> DeckService:
    deck_repository = DeckRepositoryImpl(db_session, cache)
    profile_repository = ProfileRepositoryImpl(db_session)
    swipe_client = SwipeClient(settings.swipe.url)
    return DeckService(deck_repository, profile_repository, swipe_client)
