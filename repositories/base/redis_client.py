from config import Config
from typing import Optional
import redis.asyncio as redis

class RedisClient:
    def __init__(self):
        pool = redis.ConnectionPool.from_url(Config().REDIS_URL)
        self.__client = redis.Redis(connection_pool=pool)

    async def set(self, name: str, value: str):
        await self.__client.set(name, value)

    async def setex(self, name: str, time: int, value: str):
        await self.__client.setex(name, time, value)

    async def get(self, name: str) -> Optional[str]:
        result = await self.__client.get(name)
        return result.decode('utf-8') if result else None
    
    async def delete(self, name: str):
        await self.__client.delete(name)

    async def clear_cache(self):
        await self.__client.flushdb()

    async def close(self):
        await self.__client.close()

    async def disconnect(self):
        await self.__client.connection_pool.disconnect()

    def create_key(self, prefix: str, id: int) -> str:
        return f"{prefix}:{str(id)}"