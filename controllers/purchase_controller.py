from fastapi import Depends, Response

from dto import PurchaseCreateDTO
from services import PurchaseService
from utils import DataUtils, ResponseUtils


class PurchaseController:
    @staticmethod
    async def create_purchase(purchase: PurchaseCreateDTO, purchase_service: PurchaseService = Depends()) -> Response:
        await purchase_service.create_purchase(purchase)
        return await ResponseUtils.success(DataUtils.responses.purchase_created_message)

    @staticmethod
    async def get_purchase(id: int, purchase_service: PurchaseService = Depends()) -> Response:
        purchase = await purchase_service.get_purchase(locals())

        return await ResponseUtils.success(DataUtils.responses.purchase_received_message, purchase.model_dump())

    @staticmethod
    async def delete_purchase(
        id: int, soft_delete: bool | None = True, purchase_service: PurchaseService = Depends()
    ) -> Response:
        await purchase_service.delete_purchase(locals(), soft_delete)
        return await ResponseUtils.success(DataUtils.responses.purchase_deleted_message.format(id=id))
