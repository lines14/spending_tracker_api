from typing import Optional
from DTO.base import BaseDTO

class SessionDTO(BaseDTO):
    id: int
    user_id: int
    host: str
    user_agent: str
    token: str
    created_at: str
    updated_at: str
    deleted_at: Optional[str]