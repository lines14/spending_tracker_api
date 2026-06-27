from sqlmodel import Field, Relationship
from typing import Optional, TYPE_CHECKING
from models.base.base_model import BaseModel
from models.base.optional_fields import WithTimestamps, WithSoftDelete

if TYPE_CHECKING:
    from .bank_account import BankAccount

class Purchase(BaseModel, WithTimestamps, WithSoftDelete, table=True):
    cost: float = Field(nullable=False)
    account_id: int = Field(index=True, nullable=False, foreign_key='bank_accounts.id')
    sub_type_id: int = Field(index=True, nullable=False, foreign_key='product_sub_types.id')

    bank_account: Optional["BankAccount"] = Relationship(back_populates="purchases")

Purchase.model_rebuild()