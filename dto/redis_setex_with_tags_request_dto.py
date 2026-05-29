from typing import List
from dto import RedisSetexRequestDTO

class RedisSetexWithTagsRequestDTO(RedisSetexRequestDTO):
    tags: List[str]