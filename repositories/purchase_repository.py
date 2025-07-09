import json
from DTO import PurchaseDTO
from typing import Optional
from models import Purchase

class PurchaseRepository:    
    async def create_purchase(self, purchase: PurchaseDTO) -> None:
        await Purchase(**purchase.model_dump()).create()

    async def get_purchase(self, id: int) -> Optional[PurchaseDTO]:
        purchase = await Purchase(id=id).get()

        if not purchase:
            return None
        
        stringified_purchase = json.dumps(purchase.to_dict(), default=str)

        return PurchaseDTO(**json.loads(stringified_purchase))

    async def delete_purchase(self, id: int) -> None:
        await Purchase(id=id).delete()