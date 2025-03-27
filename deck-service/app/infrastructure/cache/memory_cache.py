import asyncio
from datetime import datetime, timedelta
from typing import Any
from domain.repositories.cache import ICache


class MemoryCache(ICache):
    def __init__(self):
        self._cache = {}
        self._lock = asyncio.Lock()

    async def get_all_keys(self) -> list[str]:
        return list(self._cache.keys())

    async def get_all_values(self) -> list[Any]:
        return [value for value in self._cache.values()]

    async def get(self, key: str) -> Any | None:
        async with self._lock:
            if key not in self._cache:
                return None

            value, expiry = self._cache[key]
            if expiry and datetime.now() > expiry:
                del self._cache[key]
                return None

            return value

    async def set(self, key: str, value: Any, expire: int = None) -> None:
        async with self._lock:
            expiry = None
            if expire:
                expiry = datetime.now() + timedelta(seconds=expire)
            self._cache[key] = (value, expiry)

    async def delete(self, key: str) -> None:
        async with self._lock:
            if key in self._cache:
                del self._cache[key]

    async def exists(self, key: str) -> bool:
        async with self._lock:
            if key not in self._cache:
                return False

            _, expiry = self._cache[key]
            if expiry and datetime.now() > expiry:
                del self._cache[key]
                return False

            return True

    async def clear(self) -> None:
        async with self._lock:
            self._cache.clear()
