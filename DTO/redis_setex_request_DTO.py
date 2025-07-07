from DTO.base import BaseDTO

class RedisSetexRequestDTO(BaseDTO):
    name: str
    time: str
    value: str