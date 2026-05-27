from utils import DataUtils, ResponseUtils
from repositories.base.redis_client import RedisClient

class CacheService:
    def __init__(self):
        self.redis_client = RedisClient()

    async def clear_cache(self) -> None:
        await self.redis_client.clear_cache()
        
        return await ResponseUtils.success(DataUtils.responses.clear_cache_message)