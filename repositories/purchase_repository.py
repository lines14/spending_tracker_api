import json
from DTO import PurchaseDTO
from typing import Optional
from models import Purchase

class PurchaseRepository:    
    async def create_purchase(self, purchase: PurchaseDTO) -> None:
        await Purchase(**purchase.model_dump()).create()

    async def get_purchase(self, id: int) -> Optional[PurchaseDTO]:
        result = await Purchase(id=id).get()

        if not result:
            return None
        
        purchase = result.pop()
        stringified_purchase = json.dumps(purchase.to_dict(), default=str)

        return PurchaseDTO(**json.loads(stringified_purchase))

    async def delete_purchase(self, id: int, soft_delete: bool) -> None:
        await Purchase(id=id).delete(soft_delete)