from typing import List
from pydantic import BaseModel

class CacheTagger:
    @staticmethod
    def extract_tags_from_dto(dto: BaseModel) -> List[str]:
        tags = []
        for field_name, field_value in dto.__dict__.items():
            if field_value is not None:
                if isinstance(field_value, BaseModel):
                    tags.append(field_name)
                elif isinstance(field_value, list) and len(field_value) > 0 and isinstance(field_value[0], BaseModel):
                    tags.append(field_name)
                    
        return tags