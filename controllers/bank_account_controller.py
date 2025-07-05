from fastapi import Response
from DTO import BankAccountDTO
from models import BankAccount
from utils.data_utils import DataUtils
from utils.response_utils import ResponseUtils

class BankAccountController:
    async def create_bank_account(self, bank_account: BankAccountDTO) -> Response:
        new_bank_account = BankAccount(**vars(bank_account))
        await new_bank_account.create()
        return await ResponseUtils.success(DataUtils.responses.bank_account_created_message)
        
    async def get_bank_account(self, id: int) -> Response:
        existing_bank_account = await BankAccount(id=id).get()
        if existing_bank_account:
            return await ResponseUtils.success(
                DataUtils.responses.bank_account_received_message, 
                vars(BankAccountDTO(**vars(existing_bank_account)))
            )
        else:
            return await ResponseUtils.error(*DataUtils.responses.bank_account_not_found_error)

    async def delete_bank_account(self, id: int) -> Response:
        existing_bank_account = await BankAccount(id=id).get()
        if existing_bank_account:
            await BankAccount(id=existing_bank_account.id).delete()
            return await ResponseUtils.success(DataUtils.responses.bank_account_deleted_message.format(id=id))
        else:
            return await ResponseUtils.error(*DataUtils.responses.bank_account_not_found_error)