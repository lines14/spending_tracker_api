from dto.base import BaseDTO
from pydantic import field_validator

class RedisSetexRequestDTO(BaseDTO):
    name: str
    time: int
    value: str

    @field_validator('time', mode='before')
    @classmethod
    def cast_str_env_to_int(cls, value):
        if isinstance(value, str):
            return int(value)
        
        return value