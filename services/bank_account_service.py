from utils import DataUtils
from models import BankAccount, User
from dto import BankAccountDTO, BankAccountCreateDTO
from repositories.user_repository import UserRepository
from repositories.bank_account_repository import BankAccountRepository
from exceptions import UserNotFoundException, BankAccountNotFoundException

class BankAccountService:
    async def create_bank_account(self, bank_account: BankAccountCreateDTO) -> None:
        search_by = DataUtils.extract_parent_foreign_id_as_id(bank_account.model_dump(), User, BankAccount)
        user = await UserRepository().get_user(search_by)

        if not user:
            raise UserNotFoundException()
        
        await BankAccountRepository().create_bank_account(bank_account)
        
    async def get_bank_account(self, search_by: dict, with_relations: bool) -> BankAccountDTO:
        bank_account_repository = BankAccountRepository()

        bank_account = await bank_account_repository.get_bank_account(search_by, with_relations)

        if not bank_account:
            raise BankAccountNotFoundException()

        return BankAccountDTO(**bank_account.model_dump())
        
    async def get_bank_accounts(self, search_by: dict, with_relations: bool) -> list[BankAccountDTO]:
        bank_accounts = await BankAccountRepository().get_bank_accounts(search_by, with_relations)

        return [BankAccountDTO(**bank_account.model_dump()) for bank_account in bank_accounts]

    async def delete_bank_account(self, search_by: dict, soft_delete: bool) -> None:
        bank_account_repository = BankAccountRepository()
        bank_account = await bank_account_repository.get_bank_account(search_by)

        if not bank_account:
            raise BankAccountNotFoundException()
        
        await bank_account_repository.delete_bank_account(search_by, soft_delete)
        
    async def delete_all_bank_accounts(self, soft_delete: bool) -> None:
        await BankAccountRepository().delete_all_bank_accounts(soft_delete)