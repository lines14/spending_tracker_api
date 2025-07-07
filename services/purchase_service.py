from DTO import PurchaseDTO
from fastapi import Response, Request
from utils import DataUtils, ResponseUtils
from repositories.purchase_repository import PurchaseRepository
from repositories.bank_account_repository import BankAccountRepository

class PurchaseService:        
    async def create_purchase(self, request: Request, purchase: PurchaseDTO) -> Response:
        existing_bank_account = await BankAccountRepository().get_bank_account(purchase.account_id)

        if existing_bank_account:
            await PurchaseRepository().create_purchase(purchase)
            
            return await ResponseUtils.success(DataUtils.responses.purchase_created_message)
        else:
            return await ResponseUtils.error(request, *DataUtils.responses.bank_account_not_found_error)