from fastapi import Query
from typing import Optional
from dto import BankAccountCreateDTO
from fastapi import Request, Response
from services import BankAccountService

class BankAccountController:
    async def create_bank_account(request: Request, bank_account: BankAccountCreateDTO) -> Response:
        return await BankAccountService().create_bank_account(request, bank_account)

    async def get_bank_account(
        request: Request, 
        id: int, 
        with_relations: Optional[bool] = False
    ) -> Response:
        return await BankAccountService().get_bank_account(request, locals(), with_relations)
    
    async def get_bank_accounts(
        id: Optional[list[int]] = Query(None, alias="ids"),
        user_id: Optional[int] = None,
        with_relations: Optional[bool] = False
    ) -> Response:
        return await BankAccountService().get_bank_accounts(locals(), with_relations)

    async def delete_bank_account(request: Request, id: int, soft_delete: Optional[bool] = True) -> Response:
        return await BankAccountService().delete_bank_account(request, locals(), soft_delete)
    
    async def delete_all_bank_accounts(soft_delete: Optional[bool] = True) -> Response:
        return await BankAccountService().delete_all_bank_accounts(soft_delete)