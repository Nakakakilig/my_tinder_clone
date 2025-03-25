import aioredis
from config.settings import settings


class RedisCache:
    def __init__(self):
        self.redis = None

    async def connect(self):
        self.redis = await aioredis.from_url(settings.redis.url, decode_responses=True)

    async def close(self):
        if self.redis:
            await self.redis.close()

    async def get(self, key: str):
        return await self.redis.get(key)

    async def set(self, key: str, value: str, expire: int = settings.redis.expire):
        await self.redis.set(key, value, ex=expire)


redis_cache = RedisCache()
