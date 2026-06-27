from fastapi import Query
from typing import Optional
from dto import BankAccountCreateDTO
from services import BankAccountService
from utils import ResponseUtils, DataUtils
from fastapi import Request, Response, Depends

class BankAccountController:
    async def create_bank_account(
        request: Request, 
        bank_account: BankAccountCreateDTO,
        service: BankAccountService = Depends()
    ) -> Response:
        await service.create_bank_account(bank_account)

        return await ResponseUtils.success(DataUtils.responses.bank_account_created_message)

    async def get_bank_account(
        request: Request, 
        id: int, 
        with_relations: Optional[bool] = False,
        service: BankAccountService = Depends()
    ) -> Response:
        bank_account = await service.get_bank_account(locals(), with_relations)

        return await ResponseUtils.success(
            DataUtils.responses.bank_account_received_message,
            bank_account.model_dump()
        )
    
    async def get_bank_accounts(
        id: Optional[list[int]] = Query(None, alias="ids"),
        user_id: Optional[int] = None,
        with_relations: Optional[bool] = False,
        service: BankAccountService = Depends()
    ) -> Response:
        bank_accounts = await service.get_bank_accounts(locals(), with_relations)

        return await ResponseUtils.success(
            DataUtils.responses.bank_accounts_received_message, 
            [bank_account.model_dump() for bank_account in bank_accounts]
        )

    async def delete_bank_account(
        request: Request, 
        id: int, 
        soft_delete: Optional[bool] = True,
        service: BankAccountService = Depends()
    ) -> Response:
        await service.delete_bank_account(locals(), soft_delete)

        return await ResponseUtils.success(DataUtils.responses.bank_account_deleted_message.format(id=id))
    
    
    async def delete_all_bank_accounts(
        soft_delete: Optional[bool] = True,
        service: BankAccountService = Depends()
    ) -> Response:
        await service.delete_all_bank_accounts(soft_delete)

        return await ResponseUtils.success(DataUtils.responses.bank_accounts_deleted_message)