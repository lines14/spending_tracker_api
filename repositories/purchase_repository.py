from DTO import PurchaseDTO
from models import Purchase

class PurchaseRepository:    
    async def create_purchase(self, purchase: PurchaseDTO) -> None:
        await Purchase(**vars(purchase)).create()