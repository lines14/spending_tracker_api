from sqlmodel import Field
from models.base.base_model import BaseModel
from models.base.optional_fields import WithTimestamps, WithSoftDelete

class ProductType(BaseModel, WithTimestamps, WithSoftDelete, table=True):
    type: str = Field(nullable=False)
    group_id: int = Field(index=True, nullable=False, foreign_key='product_groups.id')