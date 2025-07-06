from DTO import PurchaseDTO
from services import PurchaseService
from fastapi import Request, Response

class PurchaseController:
    async def create_purchase(request: Request, purchase: PurchaseDTO) -> Response:
        purchase_service = PurchaseService()
        return await purchase_service.create_purchase(request, purchase)