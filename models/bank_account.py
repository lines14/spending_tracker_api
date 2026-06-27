from sqlmodel import Field, Relationship
from typing import Optional, TYPE_CHECKING
from models.base.base_model import BaseModel
from models.base.optional_fields import WithTimestamps, WithSoftDelete

if TYPE_CHECKING:
    from .user import User
    from .purchase import Purchase

class BankAccount(BaseModel, WithTimestamps, WithSoftDelete, table=True):
    account: str = Field(nullable=False)
    issuer_id: int = Field(nullable=False, foreign_key='bank_account_issuers.id')
    currency_id: int = Field(index=True, nullable=False, foreign_key='currencies.id')
    user_id: int = Field(index=True, nullable=False, foreign_key='users.id')

    user: Optional["User"] = Relationship(back_populates="bank_accounts")
    
    purchases: list["Purchase"] = Relationship(
        back_populates="bank_account", 
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

BankAccount.model_rebuild()