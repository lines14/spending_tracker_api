import sys
import json
import traceback
from DTO import StackElementDTO
from utils.logger import Logger
from fastapi import Request, Response
from utils.response_utils import ResponseUtils
from starlette.middleware.base import BaseHTTPMiddleware

class LogErrorsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
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
            error_info = {
                "message": str(exc_value),
                "stack": stack
            }

            Logger.log(json.dumps(error_info, indent=2))
            try:
                error_response = json.loads(str(e))
                return await ResponseUtils.error(*error_response)
            except:
                return await ResponseUtils.error(str(e))