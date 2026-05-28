from config import Config
import redis as sync_redis
from typing import List, Optional
import redis.asyncio as async_redis

class RedisClient:
    def __init__(self):
        sync_pool = sync_redis.ConnectionPool.from_url(Config().REDIS_URL)
        async_pool = async_redis.ConnectionPool.from_url(Config().REDIS_URL)
        self.__sync_client = sync_redis.Redis(connection_pool=sync_pool)
        self.__async_client = async_redis.Redis(connection_pool=async_pool)

    def create_key(self, prefix: str, id: Optional[int] = None) -> str:
        return f"{prefix}:{str(id)}" if id else f"{prefix}"
    
    def sync_delete(self, name: str):
        self.__sync_client.delete(name)

    def sync_clear_cache(self):
        self.__sync_client.flushdb()
    
    async def set(self, name: str, value: str):
        await self.__async_client.set(name, value)

    async def setex(self, name: str, time: int, value: str):
        await self.__async_client.setex(name, time, value)

    async def get(self, name: str) -> Optional[str]:
        result = await self.__async_client.get(name)
        return result.decode('utf-8') if result else None
    
    async def delete(self, name: str):
        await self.__async_client.delete(name)

    async def clear_cache(self):
        await self.__async_client.flushdb()

    async def close(self):
        await self.__async_client.close()

    async def disconnect(self):
        await self.__async_client.connection_pool.disconnect()

    async def set_with_tags(self, key: str, value: str, tags: List[str], ttl: Optional[int] = None) -> None:
        async with self.__async_client.pipeline(transaction=True) as pipe:
            if ttl:
                pipe.setex(key, ttl, value)
            else:
                pipe.set(key, value)
            
            for tag in tags:
                tag_key = f"tag:{tag}"
                pipe.sadd(tag_key, key)
                if ttl:
                    pipe.expire(tag_key, ttl + 300) 
            
            await pipe.execute()

    async def invalidate_tag(self, tag: str) -> None:
        tag_key = f"tag:{tag}"

        async with self.__async_client.pipeline(transaction=True) as pipe:
            keys_to_delete = await self.__async_client.smembers(tag_key)
            if keys_to_delete:
                decoded_keys = [k.decode('utf-8') for k in keys_to_delete]
                pipe.delete(*decoded_keys)
            
            pipe.delete(tag_key)
            await pipe.execute()