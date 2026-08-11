import json
from os import getenv

from dto import PurchaseDTO, RedisSetexRequestDTO
from models.purchase import Purchase
from repositories.base.base_repository import BaseRepository
from repositories.base.redis_client import RedisClient
from utils import DataUtils


class PurchaseRepository(BaseRepository):
    def __init__(self, **kwargs):
        super().__init__(Purchase, **kwargs)

    async def create_purchase(self, purchase_dto: PurchaseDTO) -> None:
        purchase = self.model(**purchase_dto.model_dump())
        await self.create(purchase)

    async def get_purchase(self, search_by: dict, with_soft_deleted: bool = False) -> PurchaseDTO | None:
        redis_client = RedisClient()

        search_by = DataUtils.filter_search_fields(search_by, self.model)
        key = redis_client.create_key("purchase", DataUtils.dict_to_model(search_by).id)
        stringified_purchase = None if with_soft_deleted else await redis_client.get(key)

        if not stringified_purchase:
            result = await self.get_one_or_none(search_by, with_soft_deleted)

            if not result:
                return None

            stringified_purchase = json.dumps(result.model_dump(), default=str)

            data = RedisSetexRequestDTO(name=key, time=getenv("FIN_DATA_TTL"), value=stringified_purchase)

            if not with_soft_deleted:
                await redis_client.setex(**data.model_dump())

        return PurchaseDTO(**json.loads(stringified_purchase))

    async def delete_purchase(self, search_by: dict, soft_delete: bool) -> None:
        search_by = DataUtils.filter_search_fields(search_by, self.model)
        await self.delete(soft_delete, search_by)
