from DTO.base import BaseDTO

class ReceiveDTO(BaseDTO):
    type: str
    body: dict
    more_body: bool