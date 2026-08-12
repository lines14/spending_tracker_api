import json
import sys
import traceback

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from db.base.base_db import BaseDB
from dto import ErrorInfoDTO, ReceiveDTO, StackElementDTO
from errors.base.base_custom_error import BaseCustomError
from models import ErrorLog
from utils import DataUtils, Logger, ResponseUtils


class LogErrorsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        body_bytes = await request.body()

        async def receive():
            receive = ReceiveDTO(type="http.request", body=json.loads(body_bytes), more_body=False)

            return receive.model_dump()

        request = Request(request.scope, receive)

        try:
            return await call_next(request)
        except BaseCustomError as bce:
            return await ResponseUtils.error(request=None, msg=bce.message, data=bce.data, status_code=bce.status_code)
        except Exception as e:
            if isinstance(e, (AttributeError, KeyError)):
                e = ValueError(DataUtils.responses.invalid_relationship_path_error_message.format(key=e))

            stack = []
            _exc_type, exc_value, exc_tb = sys.exc_info()
            stack_summary = traceback.extract_tb(exc_tb)

            for frame in stack_summary:
                stack_element = StackElementDTO(file=frame.filename, line=frame.lineno, snippet=frame.line)

                stack.append(stack_element.model_dump())

            stack.reverse()

            error_info = ErrorInfoDTO(message=str(exc_value), stack=stack)

            Logger.log("\n" + "-" * 100 + "\n")
            Logger.log(json.dumps(error_info.model_dump(), indent=2))

            formatted_stack = "[\n" + ",\n".join(json.dumps(stack_element) for stack_element in stack) + "\n]"

            error_log = ErrorLog(
                file=DataUtils.dict_to_model(stack[0]).file,
                line=DataUtils.dict_to_model(stack[0]).line,
                snippet=DataUtils.dict_to_model(stack[0]).snippet,
                stack=formatted_stack,
                message=str(exc_value),
            )

            async with BaseDB.engine.begin() as conn:
                await conn.run_sync(lambda sync_conn: sync_conn.execute(ErrorLog.__table__.insert().values(**error_log.model_dump())))

            try:
                error_response = json.loads(str(e))
                return await ResponseUtils.error(None, *error_response)
            except Exception:
                return await ResponseUtils.error(None, str(e), stack)
