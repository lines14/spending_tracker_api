from DTO import PurchaseDTO
from fastapi import Response, Request
from models import Purchase, BankAccount
from utils import DataUtils, ResponseUtils

class PurchaseService:
    async def create_purchase(self, request: Request, purchase: PurchaseDTO) -> Response:
        existing_bank_account = await BankAccount(id=purchase.account_id).get()

        if existing_bank_account:
            new_purchase = Purchase(**vars(purchase))
            await new_purchase.create()
            
            return await ResponseUtils.success(DataUtils.responses.purchase_created_message)
        else:
            return await ResponseUtils.error(request, *DataUtils.responses.bank_account_not_found_error)