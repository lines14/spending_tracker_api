from dto import RedisSetexRequestDTO


class RedisSetexWithTagsRequestDTO(RedisSetexRequestDTO):
    tags: list[str]
