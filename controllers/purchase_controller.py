from typing import Optional
from dto import PurchaseCreateDTO
from services import PurchaseService
from fastapi import Request, Response, Depends

class PurchaseController:
    async def create_purchase(
        request: Request, 
        purchase: PurchaseCreateDTO,
        service: PurchaseService = Depends()
    ) -> Response:
        return await service.create_purchase(request, purchase)
    
    async def get_purchase(
        request: Request, 
        id: int,
        service: PurchaseService = Depends()
    ) -> Response:
        return await service.get_purchase(request, locals())

    async def delete_purchase(
        request: Request, 
        id: int, 
        soft_delete: Optional[bool] = True,
        service: PurchaseService = Depends()
    ) -> Response:
        return await service.delete_purchase(request, locals(), soft_delete)