import sys
import json
import traceback
from models import ErrorLog
from fastapi import Request, Response
from utils import Logger, ResponseUtils, DataUtils
from starlette.middleware.base import BaseHTTPMiddleware
from dto import StackElementDTO, ErrorInfoDTO, ReceiveDTO
from repositories.base.base_repository import BaseRepository
from exceptions.base.base_custom_exception import BaseCustomException

class LogErrorsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.error_log_repository = BaseRepository(model=ErrorLog)

    async def dispatch(self, request: Request, call_next) -> Response:
        body_bytes = await request.body()

        async def receive():
            receive = ReceiveDTO(
                type="http.request", 
                body=json.loads(body_bytes), 
                more_body=False
            )

            return receive.model_dump()
        
        request = Request(request.scope, receive)
        
        try:
            return await call_next(request)
        except BaseCustomException as bce:
            return await ResponseUtils.error(
                request=None, 
                msg=bce.message, 
                data=bce.data,
                status_code=bce.status_code
            )
        except Exception as e:
            if isinstance(e, (AttributeError, KeyError)):
                e = ValueError(DataUtils.responses.invalid_relationship_path_error_message.format(key=e))
                
            stack = []
            exc_type, exc_value, exc_tb = sys.exc_info()
            stack_summary = traceback.extract_tb(exc_tb)

            for frame in stack_summary:
                stack_element = StackElementDTO(
                    file=frame.filename, 
                    line=frame.lineno, 
                    snippet=frame.line
                )

                stack.append(stack_element.model_dump())

            stack.reverse()

            error_info = ErrorInfoDTO(
                message=str(exc_value), 
                stack=stack
            )

            Logger.log('\n' + '-' * 100 + '\n')
            Logger.log(json.dumps(error_info.model_dump(), indent=2))

            formatted_stack = "[\n" + ",\n".join(json.dumps(stack_element) for stack_element in stack) + "\n]"
            
            error_log = ErrorLog(
                file=DataUtils.dict_to_model(stack[0]).file,
                line=DataUtils.dict_to_model(stack[0]).line,
                snippet=DataUtils.dict_to_model(stack[0]).snippet,
                stack=formatted_stack,
                message=str(exc_value)
            )

            await self.error_log_repository.create(error_log)

            try:
                error_response = json.loads(str(e))
                
                return await ResponseUtils.error(None, *error_response)
            except:
                return await ResponseUtils.error(None, str(e), stack)