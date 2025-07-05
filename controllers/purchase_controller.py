from DTO import PurchaseDTO
from fastapi import Response
from utils.data_utils import DataUtils
from models import Purchase, BankAccount
from utils.response_utils import ResponseUtils

class PurchaseController:
    async def create_purchase(self, purchase: PurchaseDTO) -> Response:
        new_purchase = Purchase(**vars(purchase))
        existing_bank_account = await BankAccount(id=new_purchase.account_id).get()
        if existing_bank_account:
            await new_purchase.create()
            return await ResponseUtils.success(DataUtils.responses.purchase_created_message)
        else:
            return await ResponseUtils.error(*DataUtils.responses.bank_account_not_found_error)