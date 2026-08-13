from repositories.base.redis_client import RedisClient


class CacheService:
    async def clear_cache(self) -> None:
        await RedisClient.get_instance().clear_cache()
