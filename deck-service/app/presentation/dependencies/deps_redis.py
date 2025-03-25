from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from infrastructure.redis.redis_cache import redis_cache

if TYPE_CHECKING:
    from infrastructure.redis.redis_cache import RedisCache


async def get_redis_cache():
    """Function for FastAPI Depends()"""
    if not redis_cache.redis:
        await redis_cache.connect()
    return redis_cache


redis_dependency = Annotated[RedisCache, Depends(get_redis_cache)]
