from dto.base import BaseDTO

class RedisSetRequestDTO(BaseDTO):
    name: str
    value: str