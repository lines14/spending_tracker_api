from fastapi import Depends

from dto import PurchaseCreateDTO, PurchaseDTO
from errors import BankAccountNotFoundError, PurchaseNotFoundError
from models import BankAccount, Purchase
from repositories.bank_account_repository import BankAccountRepository
from repositories.purchase_repository import PurchaseRepository
from utils import DataUtils


class PurchaseService:
    def __init__(
        self,
        purchase_repository: PurchaseRepository = Depends(),
        bank_account_repository: BankAccountRepository = Depends(),
    ):
        self.purchase_repository = purchase_repository
        self.bank_account_repository = bank_account_repository

    async def create_purchase(self, purchase: PurchaseCreateDTO) -> None:
        search_by = DataUtils.extract_parent_foreign_id_as_id(purchase.model_dump(), BankAccount, Purchase)
        bank_account = await self.bank_account_repository.get_bank_account(search_by)

        if not bank_account:
            raise BankAccountNotFoundError()

        await self.purchase_repository.create_purchase(purchase)

    async def get_purchase(self, search_by: dict) -> PurchaseDTO:
        purchase = await self.purchase_repository.get_purchase(search_by)

        if not purchase:
            raise PurchaseNotFoundError()

        return PurchaseDTO(**purchase.model_dump())

    async def delete_purchase(self, search_by: dict, soft_delete: bool) -> None:
        purchase = await self.purchase_repository.get_purchase(search_by)

        if not purchase:
            raise PurchaseNotFoundError()

        await self.purchase_repository.delete_purchase(search_by, soft_delete)
