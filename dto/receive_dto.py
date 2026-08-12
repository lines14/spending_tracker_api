from dto.base import BaseDTO


class ReceiveDTO(BaseDTO):
    type: str
    body: bytes
    more_body: bool
