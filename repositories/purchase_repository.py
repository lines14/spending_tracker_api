import json
from DTO import PurchaseDTO
from typing import Optional
from models import Purchase

class PurchaseRepository:    
    async def create_purchase(self, purchase: PurchaseDTO) -> None:
        await Purchase(**purchase.model_dump()).create()

    async def get_purchase(self, search_by: dict) -> Optional[PurchaseDTO]:
        result = await Purchase(**search_by).get()

        if not result:
            return None
        
        purchase = result.pop()
        stringified_purchase = json.dumps(purchase.model_dump(), default=str)

        return PurchaseDTO(**json.loads(stringified_purchase))

    async def delete_purchase(self, search_by: dict, soft_delete: bool) -> None:
        await Purchase(**search_by).delete(soft_delete)