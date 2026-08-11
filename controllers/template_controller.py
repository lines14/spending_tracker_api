from sys import version

from fastapi import Request, Response, __version__
from fastapi.templating import Jinja2Templates

from dto import ResponseTemplateContextDTO, ResponseTemplateDTO


class TemplateController:
    @staticmethod
    async def get_template(request: Request) -> Response:
        data = ResponseTemplateContextDTO(request=request, python_version=version, fastapi_version=__version__)

        templates = Jinja2Templates(directory="../templates")
        template = templates.TemplateResponse("index.html", data.model_dump())
        ResponseTemplateDTO(**vars(template))

        return template
