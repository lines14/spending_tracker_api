from pydantic import StrictBool

from dto.base import BaseDTO


class ResponseContentDTO(BaseDTO):
    success: StrictBool
    message: str
    data: str | dict | list
