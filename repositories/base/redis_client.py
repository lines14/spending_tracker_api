import redis as sync_redis
import redis.asyncio as async_redis

from config import Config


class RedisClient:
    __sync_pool = sync_redis.ConnectionPool.from_url(Config().redis_url)
    __async_pool = async_redis.ConnectionPool.from_url(Config().redis_url)

    def __init__(self):
        self.__sync_client = sync_redis.Redis(connection_pool=self.__sync_pool)
        self.__async_client = async_redis.Redis(connection_pool=self.__async_pool)

    def create_key(self, prefix: str, id: int | None = None) -> str:
        return f"{prefix}:{id!s}" if id else f"{prefix}"

    def sync_delete(self, name: str):
        self.__sync_client.delete(name)

    def sync_clear_cache(self):
        self.__sync_client.flushdb()

    async def set(self, name: str, value: str):
        await self.__async_client.set(name, value)

    async def setex(self, name: str, time: int, value: str):
        await self.__async_client.setex(name, time, value)

    async def get(self, name: str) -> str | None:
        result = await self.__async_client.get(name)
        return result.decode("utf-8") if result else None

    async def delete(self, name: str):
        await self.__async_client.delete(name)

    async def clear_cache(self):
        await self.__async_client.flushdb()

    async def close(self):
        await self.__async_client.close()

    async def disconnect(self):
        await self.__async_client.connection_pool.disconnect()

    async def setex_with_tags(self, name: str, value: str, tags: list[str], time: int | None = None) -> None:
        async with self.__async_client.pipeline(transaction=True) as pipe:
            if time:
                pipe.setex(name, time, value)
            else:
                pipe.set(name, value)

            for tag in tags:
                tag_key = f"tag:{tag}"
                pipe.sadd(tag_key, name)
                if time:
                    pipe.expire(tag_key, time + 300)

            await pipe.execute()

    async def invalidate_tag(self, tag: str) -> None:
        tag_key = f"tag:{tag}"

        async with self.__async_client.pipeline(transaction=True) as pipe:
            keys_to_delete = await self.__async_client.smembers(tag_key)
            if keys_to_delete:
                decoded_keys = [k.decode("utf-8") for k in keys_to_delete]
                pipe.delete(*decoded_keys)

            pipe.delete(tag_key)
            await pipe.execute()

    async def delete_by_prefix(self, prefix: str) -> None:
        async for key in self.__async_client.scan_iter(prefix):
            await self.__async_client.delete(key)
