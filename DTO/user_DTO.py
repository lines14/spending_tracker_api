from pydantic import Field
from typing import Optional
from DTO.base import BaseDTO
from DTO.bank_account_DTO import BankAccountDTO

class UserDTO(BaseDTO):
    id: int
    login: str
    hashed_password: str
    created_at: str
    updated_at: str
    deleted_at: Optional[str]
    bank_accounts: list[BankAccountDTO] = Field(default_factory=list)