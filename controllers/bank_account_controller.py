from typing import Optional
from DTO import BankAccountCreateDTO
from fastapi import Request, Response
from services import BankAccountService

class BankAccountController:
    async def create_bank_account(request: Request, bank_account: BankAccountCreateDTO) -> Response:
        return await BankAccountService().create_bank_account(request, bank_account)

    async def get_bank_account(request: Request, id: int) -> Response:
        return await BankAccountService().get_bank_account(request, locals())
    
    async def get_all_bank_accounts() -> Response:
        return await BankAccountService().get_all_bank_accounts()

    async def delete_bank_account(request: Request, id: int, soft_delete: Optional[bool] = True) -> Response:
        return await BankAccountService().delete_bank_account(request, locals(), soft_delete)
    
    async def delete_all_bank_accounts(soft_delete: Optional[bool] = True) -> Response:
        return await BankAccountService().delete_all_bank_accounts(soft_delete)