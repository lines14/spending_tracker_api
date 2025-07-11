from fastapi import Request, Response
from utils import DataUtils, ResponseUtils
from DTO import BankAccountDTO, BankAccountCreateDTO
from repositories.user_repository import UserRepository
from repositories.bank_account_repository import BankAccountRepository

class BankAccountService:
    async def create_bank_account(self, request: Request, bank_account: BankAccountCreateDTO) -> Response:
        existing_user = await UserRepository().get_user(bank_account.user_id)

        if existing_user:
            await BankAccountRepository().create_bank_account(bank_account)
            
            return await ResponseUtils.success(DataUtils.responses.bank_account_created_message)
        else:
            return await ResponseUtils.error(request, *DataUtils.responses.user_not_found_error)
        
    async def get_bank_account(self, request: Request, id: int) -> Response:
        existing_bank_account = await BankAccountRepository().get_bank_account(id)

        if existing_bank_account:
            return await ResponseUtils.success(
                DataUtils.responses.bank_account_received_message, 
                BankAccountDTO(**existing_bank_account.model_dump()).model_dump()
            )
        else:
            return await ResponseUtils.error(request, *DataUtils.responses.bank_account_not_found_error)

    async def delete_bank_account(self, request: Request, id: int, soft_delete: bool) -> Response:
        bank_account_repository = BankAccountRepository()
        existing_bank_account = await bank_account_repository.get_bank_account(id)

        if existing_bank_account:
            await bank_account_repository.delete_bank_account(id, soft_delete)
            
            return await ResponseUtils.success(DataUtils.responses.bank_account_deleted_message.format(id=id))
        else:
            return await ResponseUtils.error(request, *DataUtils.responses.bank_account_not_found_error)