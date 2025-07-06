from DTO import BankAccountDTO
from fastapi import Request, Response
from services import BankAccountService

class BankAccountController:
    async def create_bank_account(bank_account: BankAccountDTO) -> Response:
        return await BankAccountService().create_bank_account(bank_account)

    async def get_bank_account(request: Request, id: int) -> Response:
        return await BankAccountService().get_bank_account(request, id)

    async def delete_bank_account(request: Request, id: int) -> Response:
        return await BankAccountService().delete_bank_account(request, id)