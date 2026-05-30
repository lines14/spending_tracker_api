import json
from utils import DataUtils
from typing import Optional
from models.purchase import Purchase
from dto import PurchaseDTO, RedisSetRequestDTO
from repositories.base.redis_client import RedisClient
from repositories.base.base_repository import BaseRepository

class PurchaseRepository(BaseRepository):    
    def __init__(self):
        super().__init__(model=Purchase)

    async def create_purchase(self, purchase_dto: PurchaseDTO) -> None:
        purchase = self.model(**purchase_dto.model_dump())
        await self.create(purchase)

    async def get_purchase(self, search_by: dict) -> Optional[PurchaseDTO]:
        redis_client = RedisClient()

        search_by = DataUtils.filter_search_fields(search_by, self.model)
        key = redis_client.create_key('purchase', DataUtils.dict_to_model(search_by).id)
        stringified_purchase = await redis_client.get(key)

        if not stringified_purchase:
            result = await self.get_one_or_none(search_by)

            if not result:
                return None

            stringified_purchase = json.dumps(result.model_dump(), default=str)

            data = RedisSetRequestDTO(
                name=key, 
                value=stringified_purchase
            )

            await redis_client.set(**data.model_dump())

        return PurchaseDTO(**json.loads(stringified_purchase))

    async def delete_purchase(self, search_by: dict, soft_delete: bool) -> None:
        search_by = DataUtils.filter_search_fields(search_by, self.model)
        await self.delete(soft_delete, search_by)