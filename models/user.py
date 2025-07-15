from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship
from models.base.base_model import BaseModel

if TYPE_CHECKING:
    from .bank_account import BankAccount

class User(BaseModel, table=True):
    login: str = Field(index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    
    bank_accounts: list["BankAccount"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

User.model_rebuild()