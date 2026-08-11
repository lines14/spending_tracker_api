import json

from fastapi import Response

from db.base.base_db import BaseDB
from dto.response_content_dto import ResponseContentDTO
from dto.response_dto import ResponseDTO
from models import ErrorLog
from repositories.base.base_repository import BaseRepository


class ResponseUtils:
    @staticmethod
    async def success(
        msg: str = "", data: str | dict | list = "", status_code: int = 200, media_type="application/json"
    ) -> Response:
        content = ResponseContentDTO(success=True, message=msg, data=data)

        response = ResponseDTO(content=json.dumps(content.model_dump()), media_type=media_type, status_code=status_code)

        return Response(**response.model_dump())

    @staticmethod
    async def error(
        request, msg: str = "", data: str | dict | list = "", status_code: int = 400, media_type="application/json"
    ) -> Response:
        content = ResponseContentDTO(success=False, message=msg, data=data)

        response = ResponseDTO(content=json.dumps(content.model_dump()), media_type=media_type, status_code=status_code)

        if request:
            if request.method == "POST":
                body = await request.json()
            else:
                body = dict(request.query_params)

            error_log = ErrorLog(
                url=str(request.url), body=json.dumps(body), code=status_code, method_type=request.method, message=msg
            )

            async with BaseDB() as db:
                await BaseRepository(ErrorLog, db.session).create(error_log)

        return Response(**response.model_dump())
