from fastapi import Response, Request
from utils import DataUtils, ResponseUtils
from DTO import PurchaseDTO, PurchaseCreateDTO
from repositories.purchase_repository import PurchaseRepository
from repositories.bank_account_repository import BankAccountRepository

class PurchaseService:        
    async def create_purchase(self, request: Request, purchase: PurchaseCreateDTO) -> Response:
        existing_bank_account = await BankAccountRepository().get_bank_account(purchase.account_id)

        if existing_bank_account:
            await PurchaseRepository().create_purchase(purchase)
            
            return await ResponseUtils.success(DataUtils.responses.purchase_created_message)
        else:
            return await ResponseUtils.error(request, *DataUtils.responses.bank_account_not_found_error)
        
    async def get_purchase(self, request: Request, id: int) -> Response:
        existing_purchase = await PurchaseRepository().get_purchase(id)

        if existing_purchase:
            return await ResponseUtils.success(
                DataUtils.responses.purchase_received_message, 
                PurchaseDTO(**existing_purchase.model_dump()).model_dump()
            )
        else:
            return await ResponseUtils.error(request, *DataUtils.responses.purchase_not_found_error)

    async def delete_purchase(self, request: Request, id: int) -> Response:
        purchase_repository = PurchaseRepository()
        existing_purchase = await purchase_repository.get_purchase(id)

        if existing_purchase:
            await purchase_repository.delete_purchase(id)
            
            return await ResponseUtils.success(DataUtils.responses.purchase_deleted_message.format(id=id))
        else:
            return await ResponseUtils.error(request, *DataUtils.responses.purchase_not_found_error)