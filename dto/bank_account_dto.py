from pydantic import Field

from dto.bank_account_create_dto import BankAccountCreateDTO
from dto.purchase_dto import PurchaseDTO


class BankAccountDTO(BankAccountCreateDTO):
    id: int
    created_at: str
    updated_at: str
    deleted_at: str | None
    purchases: list[PurchaseDTO] = Field(default_factory=list)
