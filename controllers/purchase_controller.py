from typing import Optional
from dto import PurchaseCreateDTO
from services import PurchaseService
from utils import DataUtils, ResponseUtils
from fastapi import Request, Response, Depends

class PurchaseController:
    async def create_purchase(
        request: Request, 
        purchase: PurchaseCreateDTO,
        service: PurchaseService = Depends()
    ) -> Response:
        await service.create_purchase(purchase)

        return await ResponseUtils.success(DataUtils.responses.purchase_created_message)
    
    async def get_purchase(
        request: Request, 
        id: int,
        service: PurchaseService = Depends()
    ) -> Response:
        purchase = await service.get_purchase(locals())
        
        return await ResponseUtils.success(
            DataUtils.responses.purchase_received_message, 
            purchase.model_dump()
        )

    async def delete_purchase(
        request: Request, 
        id: int, 
        soft_delete: Optional[bool] = True,
        service: PurchaseService = Depends()
    ) -> Response:
        await service.delete_purchase(locals(), soft_delete)

        return await ResponseUtils.success(DataUtils.responses.purchase_deleted_message.format(id=id))