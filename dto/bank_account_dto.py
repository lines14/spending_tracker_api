from pydantic import Field
from typing import Optional
from dto.purchase_dto import PurchaseDTO
from dto.bank_account_create_dto import BankAccountCreateDTO

class BankAccountDTO(BankAccountCreateDTO):
    id: int
    created_at: str
    updated_at: str
    deleted_at: Optional[str]
    purchases: list[PurchaseDTO] = Field(default_factory=list)