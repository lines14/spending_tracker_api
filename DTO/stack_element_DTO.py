from DTO.base import BaseDTO

class StackElementDTO(BaseDTO):
    file: str
    line: int
    snippet: str