from typing import Optional
from DTO import BankAccountCreateDTO
from fastapi import Request, Response
from services import BankAccountService

class BankAccountController:
    async def create_bank_account(request: Request, bank_account: BankAccountCreateDTO) -> Response:
        return await BankAccountService().create_bank_account(request, bank_account)

    async def get_bank_account(request: Request, id: int) -> Response:
        return await BankAccountService().get_bank_account(request, id)

    async def delete_bank_account(request: Request, id: int, soft_delete: Optional[bool] = True) -> Response:
        return await BankAccountService().delete_bank_account(request, id, soft_delete)