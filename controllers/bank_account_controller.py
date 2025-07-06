from DTO import BankAccountDTO
from fastapi import Request, Response
from services import BankAccountService

class BankAccountController:
    async def create_bank_account(bank_account: BankAccountDTO) -> Response:
        bank_account_service = BankAccountService()
        return await bank_account_service.create_bank_account(bank_account)

    async def get_bank_account(request: Request, id: int) -> Response:
        bank_account_service = BankAccountService()
        return await bank_account_service.get_bank_account(request, id)

    async def delete_bank_account(request: Request, id: int) -> Response:
        bank_account_service = BankAccountService()
        return await bank_account_service.delete_bank_account(request, id)