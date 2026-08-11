from fastapi import Depends

from dto import BankAccountCreateDTO, BankAccountDTO
from errors import BankAccountNotFoundError, UserNotFoundError
from models import BankAccount, User
from repositories.bank_account_repository import BankAccountRepository
from repositories.user_repository import UserRepository
from utils import DataUtils


class BankAccountService:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        bank_account_repository: BankAccountRepository = Depends(),
    ):
        self.user_repository = user_repository
        self.bank_account_repository = bank_account_repository

    async def create_bank_account(self, bank_account: BankAccountCreateDTO) -> None:
        search_by = DataUtils.extract_parent_foreign_id_as_id(bank_account.model_dump(), User, BankAccount)
        user = await self.user_repository.get_user(search_by)

        if not user:
            raise UserNotFoundError()

        await self.bank_account_repository.create_bank_account(bank_account)

    async def get_bank_account(self, search_by: dict, with_relations: bool) -> BankAccountDTO:
        bank_account = await self.bank_account_repository.get_bank_account(search_by, with_relations)

        if not bank_account:
            raise BankAccountNotFoundError()

        return BankAccountDTO(**bank_account.model_dump())

    async def get_bank_accounts(self, search_by: dict, with_relations: bool) -> list[BankAccountDTO]:
        bank_accounts = await self.bank_account_repository.get_bank_accounts(search_by, with_relations)
        return [BankAccountDTO(**bank_account.model_dump()) for bank_account in bank_accounts]

    async def delete_bank_account(self, search_by: dict, soft_delete: bool) -> None:
        bank_account = await self.bank_account_repository.get_bank_account(search_by)

        if not bank_account:
            raise BankAccountNotFoundError()

        await self.bank_account_repository.delete_bank_account(search_by, soft_delete)

    async def delete_all_bank_accounts(self, soft_delete: bool) -> None:
        await self.bank_account_repository.delete_all_bank_accounts(soft_delete)
