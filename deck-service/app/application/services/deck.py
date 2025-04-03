from domain.models.deck import MatchDeck
from domain.repositories.deck import IDeckRepository


class DeckService:
    def __init__(
        self,
        deck_repository: IDeckRepository,
    ):
        self.deck_repository = deck_repository

    async def get_deck_by_id(self, profile_id: int) -> MatchDeck:
        return await self.deck_repository.get_deck_by_id(profile_id)

    async def generate_deck_by_id(self, profile_id: int, limit: int) -> MatchDeck:
        return await self.deck_repository.generate_deck_by_id(profile_id, limit)

    async def get_all_decks(self) -> list[MatchDeck]:
        return await self.deck_repository.get_all_decks()

    async def clear_deck_cache_by_id(self, profile_id: int) -> None:
        return await self.deck_repository.clear_deck_cache_by_id(profile_id)

    async def clear_all_deck_cache(self) -> None:
        return await self.deck_repository.clear_all_deck_cache()
