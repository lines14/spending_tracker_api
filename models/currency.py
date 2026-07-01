from sqlmodel import Field

from models.base.base_model import BaseModel
from models.base.optional_fields import WithSoftDelete, WithTimestamps


class Currency(BaseModel, WithTimestamps, WithSoftDelete, table=True):
    __tablename__ = 'currencies'
    currency: str = Field(nullable=False)
