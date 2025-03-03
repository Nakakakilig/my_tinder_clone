from typing import Annotated, Any

from fastapi import Depends


class DeckCache:
    def __init__(self):
        self.store = {}

    async def set_deck(self, profile_id: int, deck_data: Any):
        self.store[profile_id] = deck_data

    async def get_deck(self, profile_id: int):
        return self.store.get(profile_id)


def get_deck_cache():
    return DeckCache()


deck_dependency = Annotated[DeckCache, Depends(get_deck_cache)]
