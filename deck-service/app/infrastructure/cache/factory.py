from redis import asyncio as aioredis

from domain.repositories.cache import ICache
from infrastructure.cache.memory_cache import MemoryCache
from infrastructure.cache.redis_cache import RedisCache


class CacheFactory:
    @staticmethod
    def create_memory_cache() -> ICache:
        return MemoryCache()

    @staticmethod
    def create_redis_cache(redis_client: aioredis.Redis) -> ICache:
        return RedisCache(redis_client)
