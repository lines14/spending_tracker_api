from typing import List, Optional
from pydantic import field_validator
from dto import RedisSetexRequestDTO

class RedisSetexWithTagsRequestDTO(RedisSetexRequestDTO):
    tags: List[str]
    time: Optional[int]

    @field_validator('time', mode='before')
    @classmethod
    def cast_str_env_to_int(cls, value):
        if isinstance(value, str):
            return int(value)
        
        return value