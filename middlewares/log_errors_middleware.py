import json
import traceback
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
            Logger.log(traceback.format_stack())
            try:
                error_response = json.loads(str(e))
                return await ResponseUtils.error(*error_response)
            except:
                return await ResponseUtils.error(str(e))