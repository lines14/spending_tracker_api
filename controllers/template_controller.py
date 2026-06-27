from services import TemplateService
from fastapi import Request, Response, Depends

class TemplateController:
    async def get_template(
        request: Request, 
        service: TemplateService = Depends()
    ) -> Response:
        return await service.get_template(request)