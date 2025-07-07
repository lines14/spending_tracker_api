from DTO.base import BaseDTO

class RedisSetRequestDTO(BaseDTO):
    name: str
    value: str