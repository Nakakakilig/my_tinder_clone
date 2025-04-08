from abc import ABC, abstractmethod

from domain.models.deck import MatchDeck


class IDeckRepository(ABC):
    @abstractmethod
    async def get_deck_by_id(self, profile_id: int) -> MatchDeck:
        raise NotImplementedError

    @abstractmethod
    async def save_deck(self, deck: MatchDeck) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_decks(self, limit: int, offset: int) -> list[MatchDeck]:
        raise NotImplementedError

    @abstractmethod
    async def clear_deck_cache_by_id(self, profile_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def clear_all_deck_cache(self) -> None:
        raise NotImplementedError
