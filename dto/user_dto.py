from pydantic import Field

from dto.bank_account_dto import BankAccountDTO
from dto.base import BaseDTO


class UserDTO(BaseDTO):
    id: int
    login: str
    hashed_password: str
    created_at: str
    updated_at: str
    deleted_at: str | None
    bank_accounts: list[BankAccountDTO] = Field(default_factory=list)
