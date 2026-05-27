from pydantic import BaseModel

class BaseDTO(BaseModel):
    class Config:
        from_attributes = True
        validate_assignment = True
        arbitrary_types_allowed=True