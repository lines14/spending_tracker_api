from typing import Union
from dto.base import BaseDTO
from pydantic import StrictBool

class ResponseContentDTO(BaseDTO):
    success: StrictBool
    message: str
    data: Union[str, dict, list]