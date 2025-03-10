from typing import Annotated, Any

from core.db.db_helper import db_helper
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


class SingletonDeckCache:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.store = {}
        return cls._instance

    async def set_deck(self, profile_id: int, deck_data: Any):
        self.store[profile_id] = deck_data

    async def get_deck(self, profile_id: int):
        return self.store.get(profile_id)


def get_singleton_deck_cache():
    return SingletonDeckCache()


deck_dependency = Annotated[SingletonDeckCache, Depends(get_singleton_deck_cache)]

db_dependency = Annotated[AsyncSession, Depends(db_helper.session_getter)]
