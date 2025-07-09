from sys import version
from fastapi.templating import Jinja2Templates
from fastapi import Request, Response, __version__
from DTO import ResponseTemplateDTO, ResponseTemplateContextDTO

class TemplateService:
    async def get_template(self, request: Request) -> Response:
        data = ResponseTemplateContextDTO(
            request=request, 
            pythonVersion=version, 
            fastapiVersion=__version__
        )

        templates = Jinja2Templates(directory="../templates")
        template = templates.TemplateResponse("index.html", data.model_dump())
        ResponseTemplateDTO(**vars(template))
        
        return template