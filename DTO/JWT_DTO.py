from DTO.base import BaseDTO
from datetime import datetime

class JWTDTO(BaseDTO):
    id: int
    exp: datetime