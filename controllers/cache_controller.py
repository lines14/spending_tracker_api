from fastapi import Depends

from dto import ResponseContentDTO
from services import CacheService
from utils import DataUtils, ResponseUtils


class CacheController:
    @staticmethod
    async def clear_cache(service: CacheService = Depends()) -> ResponseContentDTO:
        await service.clear_cache()
        return await ResponseUtils.success(DataUtils.responses.clear_cache_message)
