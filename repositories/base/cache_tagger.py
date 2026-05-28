from typing import Any
from pydantic import BaseModel

class CacheTagger:
    @staticmethod
    def extract_tags_from_dto(dto: BaseModel) -> list[str]:
        tags = []
        
        def walk(obj: Any):
            if isinstance(obj, BaseModel):
                for field_name, field_value in obj.__dict__.items():
                    if field_value is not None:
                        if isinstance(field_value, BaseModel):
                            tags.append(field_name)
                            walk(field_value)
                        elif isinstance(field_value, list) and len(field_value) > 0 and isinstance(field_value[0], BaseModel):
                            tags.append(field_name)
                            for item in field_value:
                                walk(item)
                                
        walk(dto)
        return list(set(tags))