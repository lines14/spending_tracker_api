from sqlmodel import Field
from models.base.base_model import BaseModel

class ErrorLog(BaseModel, table=True):
    file: str = Field(nullable=True)
    line: int = Field(nullable=True)
    snippet: str = Field(nullable=True)
    stack: str = Field(nullable=True)
    message: str = Field(nullable=False)
    code: int = Field(nullable=True)
    method_type: str = Field(nullable=True)
    body: str = Field(nullable=True)
    url: str = Field(nullable=True)