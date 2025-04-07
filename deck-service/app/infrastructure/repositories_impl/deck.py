from sqlalchemy.ext.asyncio import AsyncSession

from domain.exceptions import DeckCacheError
from domain.models.deck import MatchDeck
from domain.repositories.cache import ICache
from domain.repositories.deck import IDeckRepository


class DeckRepositoryImpl(IDeckRepository):
    def __init__(self, db_session: AsyncSession, cache: ICache):
        self.db_session = db_session
        self.cache = cache

    async def get_deck_by_id(self, profile_id: int) -> MatchDeck:
        deck_data = await self.cache.get(f"deck:{profile_id}")
        if not deck_data:
            raise DeckCacheError(profile_id)
        return MatchDeck(**deck_data)

    async def save_deck(self, deck: MatchDeck) -> None:
        await self.cache.set(f"deck:{deck.profile_id}", deck.model_dump())
        return

    async def clear_deck_cache_by_id(self, profile_id: int) -> None:
        await self.cache.delete(f"deck:{profile_id}")
        return

    async def get_all_decks(self) -> list[MatchDeck]:
        decks_data = await self.cache.get_all_values()
        if not decks_data:
            raise DeckCacheError()
        decks = [MatchDeck(**deck_data) for deck_data in decks_data]
        sorted_decks = sorted(decks, key=lambda x: x.profile_id)
        return sorted_decks

    async def clear_all_deck_cache(self) -> None:
        await self.cache.clear()
        return
