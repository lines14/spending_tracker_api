from sqlmodel import Field
from models.base.base_model import BaseModel
from models.base.optional_fields import WithTimestamps, WithSoftDelete

class Session(BaseModel, WithTimestamps, WithSoftDelete, table=True):
    user_id: int = Field(index=True, nullable=False, foreign_key='users.id')
    host: str = Field(nullable=False)
    user_agent: str = Field(nullable=False)
    token: str = Field(nullable=False)