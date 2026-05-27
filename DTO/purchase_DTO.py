from typing import Optional
from dto.purchase_create_dto import PurchaseCreateDTO

class PurchaseDTO(PurchaseCreateDTO):
    id: int
    created_at: str
    updated_at: str
    deleted_at: Optional[str]