from abc import ABC, abstractmethod


class IDeckRepository(ABC):
    @abstractmethod
    async def get_deck_by_id(self):
        raise NotImplementedError

    @abstractmethod
    async def generate_deck_by_id(self):
        raise NotImplementedError

    @abstractmethod
    async def get_all_decks(self):
        raise NotImplementedError

    @abstractmethod
    async def clear_deck_cache_by_id(self):
        raise NotImplementedError

    @abstractmethod
    async def clear_all_deck_cache(self):
        raise NotImplementedError
