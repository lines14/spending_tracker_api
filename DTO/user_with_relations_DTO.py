from typing import Optional
from DTO.base import BaseDTO

class UserWithRelationsDTO(BaseDTO):
    id: int
    login: str
    hashed_password: str
    created_at: str
    updated_at: str
    deleted_at: Optional[str]