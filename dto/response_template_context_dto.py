from fastapi import Request

from dto.base import BaseDTO


class ResponseTemplateContextDTO(BaseDTO):
    request: Request
    python_version: str
    fastapi_version: str
