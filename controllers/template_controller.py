from services import TemplateService
from fastapi import Request, Response

class TemplateController:
    async def get_template(request: Request) -> Response:
        return await TemplateService().get_template(request)