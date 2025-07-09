from pydantic import Field
from typing import Optional
from DTO.purchase_DTO import PurchaseDTO
from DTO.bank_account_create_DTO import BankAccountCreateDTO

class BankAccountDTO(BankAccountCreateDTO):
    id: int
    created_at: str
    updated_at: str
    deleted_at: Optional[str]
    purchases: list[PurchaseDTO] = Field(default_factory=list)