from datetime import datetime

from dto.base import BaseDTO


class JWTDTO(BaseDTO):
    id: int
    exp: datetime
