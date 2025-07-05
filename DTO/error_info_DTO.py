from DTO.base import BaseDTO

class ErrorInfoDTO(BaseDTO):
    message: str
    stack: list