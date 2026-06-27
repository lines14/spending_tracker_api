from sqlmodel import Field
from models.base.base_model import BaseModel
from models.base.optional_fields import WithTimestamps, WithSoftDelete

class Currency(BaseModel, WithTimestamps, WithSoftDelete, table=True):
    __tablename__ = 'currencies'
    currency: str = Field(nullable=False)