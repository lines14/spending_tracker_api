import json
from typing import Union
from models import ErrorLog
from fastapi import Response
from DTO.response_DTO import ResponseDTO
from DTO.response_content_DTO import ResponseContentDTO

class ResponseUtils:
    @staticmethod
    async def success(
        msg: str = '', 
        data: Union[str, dict, list] = '', 
        status_code: int = 200, 
        media_type="application/json"
    ) -> Response:
        content = ResponseContentDTO(
            success=True, 
            message=msg, 
            data=data
        )

        response = ResponseDTO(
            content=json.dumps(vars(content)), 
            media_type=media_type, 
            status_code=status_code
        )

        return Response(**vars(response))

    @staticmethod
    async def error(
        request,
        msg: str = '', 
        data: Union[str, dict, list] = '', 
        status_code: int = 400, 
        media_type="application/json"
    ) -> Response:
        content = ResponseContentDTO(
            success=False, 
            message=msg, 
            data=data
        )

        response = ResponseDTO(
            content=json.dumps(vars(content)), 
            media_type=media_type, 
            status_code=status_code
        )

        if request:
            if request.method == 'POST':
                body = await request.json()
            else:
                body = dict(request.query_params)

            error_log = ErrorLog(
                url=str(request.url),
                body=json.dumps(body),
                code=status_code,
                method_type=request.method,
                message=msg
            )
            await error_log.create()

        return Response(**vars(response))