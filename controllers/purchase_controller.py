from DTO import PurchaseDTO
from services import PurchaseService
from fastapi import Request, Response

class PurchaseController:
    async def create_purchase(request: Request, purchase: PurchaseDTO) -> Response:
        return await PurchaseService().create_purchase(request, purchase)