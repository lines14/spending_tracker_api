from sqlmodel import Field

from models.base.base_model import BaseModel
from models.base.optional_fields import WithSoftDelete, WithTimestamps


class BankAccountIssuer(BaseModel, WithTimestamps, WithSoftDelete, table=True):
    issuer: str = Field(nullable=False)
    country_code: str = Field(nullable=False)
