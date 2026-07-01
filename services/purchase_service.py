from dto import PurchaseCreateDTO, PurchaseDTO
from exceptions import BankAccountNotFoundException, PurchaseNotFoundException
from models import BankAccount, Purchase
from repositories.bank_account_repository import BankAccountRepository
from repositories.purchase_repository import PurchaseRepository
from utils import DataUtils


class PurchaseService:
    async def create_purchase(self, purchase: PurchaseCreateDTO) -> None:
        search_by = DataUtils.extract_parent_foreign_id_as_id(purchase.model_dump(), BankAccount, Purchase)
        bank_account = await BankAccountRepository().get_bank_account(search_by)

        if not bank_account:
            raise BankAccountNotFoundException()

        await PurchaseRepository().create_purchase(purchase)

    async def get_purchase(self, search_by: dict) -> PurchaseDTO:
        purchase = await PurchaseRepository().get_purchase(search_by)

        if not purchase:
            raise PurchaseNotFoundException()

        return PurchaseDTO(**purchase.model_dump())


    async def delete_purchase(self, search_by: dict, soft_delete: bool) -> None:
        purchase_repository = PurchaseRepository()
        purchase = await purchase_repository.get_purchase(search_by)

        if not purchase:
            raise PurchaseNotFoundException()

        await purchase_repository.delete_purchase(search_by, soft_delete)
