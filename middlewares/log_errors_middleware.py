import sys
import json
import traceback
from models import ErrorLog
from fastapi import Request, Response
from utils import Logger, ResponseUtils, DataUtils
from starlette.middleware.base import BaseHTTPMiddleware
from DTO import StackElementDTO, ErrorInfoDTO, ReceiveDTO

class LogErrorsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        body_bytes = await request.body()

        async def receive():
            return vars(ReceiveDTO(
                type="http.request", 
                body=json.loads(body_bytes), 
                more_body=False
            ))
        
        request = Request(request.scope, receive)
        
        try:
            return await call_next(request)
        except Exception as e:
            stack = []

            exc_type, exc_value, exc_tb = sys.exc_info()
            stack_summary = traceback.extract_tb(exc_tb)

            for frame in stack_summary:
                stack_element = StackElementDTO(
                    file=frame.filename, 
                    line=frame.lineno, 
                    snippet=frame.line
                )

                stack.append(vars(stack_element))

            stack.reverse()

            error_info = ErrorInfoDTO(
                message=str(exc_value), 
                stack=stack
            )

            Logger.log('\n' + '-' * 100 + '\n')
            Logger.log(json.dumps(vars(error_info), indent=2))

            formatted_stack = "[\n" + ",\n".join(json.dumps(stack_element) for stack_element in stack) + "\n]"
            
            error_log = ErrorLog(
                file=DataUtils.dict_to_model(stack[0]).file,
                line=DataUtils.dict_to_model(stack[0]).line,
                snippet=DataUtils.dict_to_model(stack[0]).snippet,
                stack=formatted_stack,
                message=str(exc_value)
            )

            await error_log.create()

            try:
                error_response = json.loads(str(e))
                
                return await ResponseUtils.error(None, *error_response)
            except:
                return await ResponseUtils.error(None, str(e))