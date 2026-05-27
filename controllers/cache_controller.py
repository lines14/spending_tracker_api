from fastapi import Request
from services import CacheService
from dto import ResponseContentDTO

class CacheController:
    @staticmethod
    async def clear_cache() -> ResponseContentDTO:
        return await CacheService().clear_cache()