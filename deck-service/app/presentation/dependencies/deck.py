from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.services.deck import DeckService
from domain.repositories.cache import ICache
from infrastructure.repositories_impl.deck import DeckRepositoryImpl
from presentation.dependencies.cache import get_cache
from presentation.dependencies.db_session import get_db_session


def get_deck_service(
    db_session: AsyncSession = Depends(get_db_session),
    cache: ICache = Depends(get_cache),
) -> DeckService:
    deck_repository = DeckRepositoryImpl(db_session, cache)
    return DeckService(deck_repository)
