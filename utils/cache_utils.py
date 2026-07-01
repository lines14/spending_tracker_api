from typing import Any

from pydantic import BaseModel

from repositories.base.redis_client import RedisClient


class CacheUtils:
    @staticmethod
    def extract_cache_tags_from_dto(dto: BaseModel) -> list[str]:
        tags = []

        def walk(obj: Any):
            if isinstance(obj, BaseModel):
                for field_name, field_value in obj.__dict__.items():
                    if field_value is not None:
                        if isinstance(field_value, BaseModel):
                            tags.append(field_name)
                            walk(field_value)
                        elif isinstance(field_value, list) and len(field_value) > 0 and isinstance(field_value[0], BaseModel):
                            tags.append(field_name)
                            for item in field_value:
                                walk(item)

        walk(dto)
        return list(set(tags))

    @staticmethod
    async def cascade_invalidate_bank_account_cache(redis_client: RedisClient):
        prefixes = [
            f"*{redis_client.create_key('bank_account')}:*",
            f"*{redis_client.create_key('bank_account_with_relations')}:*",
            f"*{redis_client.create_key('purchase')}:*",
            f"*{redis_client.create_key('user_bank_accounts')}:*",
            f"*{redis_client.create_key('user_with_relations')}:*",
        ]

        keys = [
            "users",
            "users_with_relations",
            "bank_accounts",
            "bank_accounts_with_relations",
            "purchases"
        ]

        for prefix in prefixes:
            await redis_client.delete_by_prefix(prefix)
        for key in keys:
            await redis_client.invalidate_tag(key)
            await redis_client.delete(key)
