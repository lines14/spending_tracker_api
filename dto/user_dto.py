from pydantic import Field
from typing import Optional
from dto.base import BaseDTO
from dto.bank_account_dto import BankAccountDTO

class UserDTO(BaseDTO):
    id: int
    login: str
    hashed_password: str
    created_at: str
    updated_at: str
    deleted_at: Optional[str]
    bank_accounts: list[BankAccountDTO] = Field(default_factory=list)