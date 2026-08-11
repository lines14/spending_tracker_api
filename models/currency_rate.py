from sqlmodel import Field

from models.base.base_model import BaseModel
from models.base.optional_fields import WithSoftDelete, WithTimestamps


class CurrencyRate(BaseModel, WithTimestamps, WithSoftDelete, table=True):
    rate: float = Field(nullable=False)
    currency_id: int = Field(index=True, nullable=False, foreign_key="currencies.id")
