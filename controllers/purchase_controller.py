from DTO import PurchaseDTO
from models import Purchase
from fastapi import Response
from utils.data_utils import DataUtils
from utils.response_utils import ResponseUtils

class PurchaseController:
    async def create_purchase(self, purchase: PurchaseDTO) -> Response:
        new_purchase = Purchase(**vars(purchase))
        await new_purchase.create()
        return await ResponseUtils.success(DataUtils.responses.purchase_created_message)