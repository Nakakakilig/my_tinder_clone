import json
from typing import Any

from redis import asyncio as aioredis

from domain.repositories.cache import ICache


class RedisCache(ICache):
    def __init__(self, redis_client: aioredis.Redis):
        self._redis = redis_client

    async def get_all_keys(self) -> list[str]:
        return list(await self._redis.keys("*"))  # type: ignore

    async def get_all_values(self) -> list[Any]:
        return [json.loads(await self._redis.get(key)) for key in await self._redis.keys("*")]  # type: ignore

    async def get(self, key: str) -> Any | None:
        value = await self._redis.get(key)
        if value is None:
            return None
        return json.loads(value)

    async def set(self, key: str, value: Any, expire: int | None = None) -> None:
        value_json = json.dumps(value, ensure_ascii=False)
        if expire:
            await self._redis.setex(key, expire, value_json)
        else:
            await self._redis.set(key, value_json)

    async def delete(self, key: str) -> None:
        await self._redis.delete(key)

    async def exists(self, key: str) -> bool:
        return bool(await self._redis.exists(key))

    async def clear(self) -> None:
        # await self._redis.flushdb()
        [await self._redis.delete(key) for key in await self._redis.keys("*")]  # type: ignore
