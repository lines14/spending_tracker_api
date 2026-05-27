from models import BankAccount, User
from fastapi import Request, Response
from utils import DataUtils, ResponseUtils
from dto import BankAccountDTO, BankAccountCreateDTO
from repositories.user_repository import UserRepository
from repositories.bank_account_repository import BankAccountRepository

class BankAccountService:
    async def create_bank_account(self, request: Request, bank_account: BankAccountCreateDTO) -> Response:
        search_by = DataUtils.extract_parent_foreign_id_as_id(bank_account.model_dump(), User, BankAccount)
        existing_user = await UserRepository().get_user(search_by)

        if existing_user:
            await BankAccountRepository().create_bank_account(bank_account)
            
            return await ResponseUtils.success(DataUtils.responses.bank_account_created_message)
        else:
            return await ResponseUtils.error(request, *DataUtils.responses.user_not_found_error)
        
    async def get_bank_account(self, request: Request, search_by: dict) -> Response:
        existing_bank_account = await BankAccountRepository().get_bank_account(search_by)

        if existing_bank_account:
            return await ResponseUtils.success(
                DataUtils.responses.bank_account_received_message, 
                BankAccountDTO(**existing_bank_account.model_dump()).model_dump()
            )
        else:
            return await ResponseUtils.error(request, *DataUtils.responses.bank_account_not_found_error)
        
    async def get_all_bank_accounts(self) -> Response:
        existing_bank_accounts = await BankAccountRepository().get_all_bank_accounts()

        return await ResponseUtils.success(
            DataUtils.responses.bank_accounts_received_message, 
            [BankAccountDTO(**item.model_dump()).model_dump() for item in existing_bank_accounts]
        )

    async def delete_bank_account(self, request: Request, search_by: dict, soft_delete: bool) -> Response:
        bank_account_repository = BankAccountRepository()
        existing_bank_account = await bank_account_repository.get_bank_account(search_by)

        if existing_bank_account:
            await bank_account_repository.delete_bank_account(search_by, soft_delete)
            
            return await ResponseUtils.success(DataUtils.responses.bank_account_deleted_message.format(id=DataUtils.dict_to_model(search_by).id))
        else:
            return await ResponseUtils.error(request, *DataUtils.responses.bank_account_not_found_error)
        
    async def delete_all_bank_accounts(self, soft_delete: bool) -> Response:
        await BankAccountRepository().delete_all_bank_accounts(soft_delete)
            
        return await ResponseUtils.success(DataUtils.responses.bank_accounts_deleted_message)