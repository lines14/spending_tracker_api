from typing import Any

from pydantic import Field

from dto.base import BaseDTO
from dto.response_template_context_dto import ResponseTemplateContextDTO


class ResponseTemplateDTO(BaseDTO):
    status_code: int
    background: Any
    body: str
    context: ResponseTemplateContextDTO
    headers: dict = Field(default_factory=dict)
