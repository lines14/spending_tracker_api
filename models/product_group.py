from sqlmodel import Field
from models.base.base_model import BaseModel
from models.base.optional_fields import WithTimestamps, WithSoftDelete

class ProductGroup(BaseModel, WithTimestamps, WithSoftDelete, table=True):
    group: str = Field(nullable=False)