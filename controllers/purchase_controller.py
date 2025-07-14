from typing import Optional
from DTO import PurchaseCreateDTO
from services import PurchaseService
from fastapi import Request, Response

class PurchaseController:
    async def create_purchase(request: Request, purchase: PurchaseCreateDTO) -> Response:
        return await PurchaseService().create_purchase(request, purchase)
    
    async def get_purchase(request: Request, id: int) -> Response:
        return await PurchaseService().get_purchase(request, locals())

    async def delete_purchase(request: Request, id: int, soft_delete: Optional[bool] = True) -> Response:
        return await PurchaseService().delete_purchase(request, locals(), soft_delete)