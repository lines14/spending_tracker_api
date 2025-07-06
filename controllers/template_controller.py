from services import TemplateService
from fastapi import Request, Response

class TemplateController:
    async def get_template(request: Request) -> Response:
        template_service = TemplateService()
        return await template_service.get_template(request)