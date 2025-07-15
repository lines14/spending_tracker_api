from fastapi import Response, Request
from models import Purchase, BankAccount
from utils import DataUtils, ResponseUtils
from DTO import PurchaseDTO, PurchaseCreateDTO
from repositories.purchase_repository import PurchaseRepository
from repositories.bank_account_repository import BankAccountRepository

class PurchaseService:        
    async def create_purchase(self, request: Request, purchase: PurchaseCreateDTO) -> Response:
        search_by = DataUtils.extract_parent_foreign_id_as_id(purchase.model_dump(), BankAccount, Purchase)
        existing_bank_account = await BankAccountRepository().get_bank_accounts(search_by)

        if existing_bank_account:
            await PurchaseRepository().create_purchase(purchase)
            
            return await ResponseUtils.success(DataUtils.responses.purchase_created_message)
        else:
            return await ResponseUtils.error(request, *DataUtils.responses.bank_account_not_found_error)
        
    async def get_purchase(self, request: Request, search_by: dict) -> Response:
        existing_purchase = await PurchaseRepository().get_purchases(search_by)

        if existing_purchase:
            return await ResponseUtils.success(
                DataUtils.responses.purchase_received_message, 
                PurchaseDTO(**existing_purchase.model_dump()).model_dump()
            )
        else:
            return await ResponseUtils.error(request, *DataUtils.responses.purchase_not_found_error)

    async def delete_purchase(self, request: Request, search_by: dict, soft_delete: bool) -> Response:
        purchase_repository = PurchaseRepository()
        existing_purchase = await purchase_repository.get_purchases(search_by)

        if existing_purchase:
            await purchase_repository.delete_purchases(search_by, soft_delete)
            
            return await ResponseUtils.success(DataUtils.responses.purchase_deleted_message.format(id=DataUtils.dict_to_model(search_by).id))
        else:
            return await ResponseUtils.error(request, *DataUtils.responses.purchase_not_found_error)