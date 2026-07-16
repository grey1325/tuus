from redis.asyncio import Redis

from src.config import CACHE_TTL


class CacheService:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    async def get(self, key: str) -> str | None:
        return await self.redis_client.get(key)

    async def set(self, key: str, value: str, ttl: int = CACHE_TTL) -> bool:
        return await self.redis_client.set(key, value, ex=ttl)

    async def delete(self, key: str) -> int:
        return await self.redis_client.delete(key)

    async def delete_pattern(self, pattern: str) -> None:
        keys = await self.redis_client.keys(pattern)
        if keys:
            await self.redis_client.delete(*keys)
