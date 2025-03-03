from typing import Annotated

import aioredis
from fastapi import Depends


class RedisCache:
    def __init__(self):
        self.redis = None

    async def connect(self):
        self.redis = await aioredis.from_url(
            "redis://localhost:6379", decode_responses=True
        )

    async def close(self):
        if self.redis:
            await self.redis.close()

    async def get(self, key: str):
        return await self.redis.get(key)

    async def set(self, key: str, value: str, expire: int = 3600):
        await self.redis.set(key, value, ex=expire)


redis_cache = RedisCache()


async def get_redis_cache():
    """Function for FastAPI Depends()"""
    if not redis_cache.redis:
        await redis_cache.connect()
    return redis_cache


redis_dependency = Annotated[RedisCache, Depends(get_redis_cache)]
