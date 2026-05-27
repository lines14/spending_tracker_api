from dto.base import BaseDTO

class StackElementDTO(BaseDTO):
    file: str
    line: int
    snippet: str