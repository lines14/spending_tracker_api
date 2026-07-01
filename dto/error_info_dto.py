from dto.base import BaseDTO


class ErrorInfoDTO(BaseDTO):
    message: str
    stack: list
