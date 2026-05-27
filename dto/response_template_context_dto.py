from fastapi import Request
from dto.base import BaseDTO

class ResponseTemplateContextDTO(BaseDTO):
    request: Request
    pythonVersion: str
    fastapiVersion: str