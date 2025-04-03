from collections.abc import AsyncGenerator

from fastapi import Depends
from redis import asyncio as aioredis

from config.settings import settings
from domain.repositories.cache import ICache
from infrastructure.cache.factory import CacheFactory


async def get_redis_client() -> AsyncGenerator[aioredis.Redis, None]:
    redis = await aioredis.from_url(settings.redis.url, decode_responses=True)
    try:
        yield redis
    finally:
        await redis.close()


def get_cache(redis_client: aioredis.Redis = Depends(get_redis_client)) -> ICache:
    # return CacheFactory.create_memory_cache()
    return CacheFactory.create_redis_cache(redis_client)
