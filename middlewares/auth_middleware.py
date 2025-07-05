from DTO import JWTDTO
from config import Config
from models import User, Session
from utils.JWT_utils import JWTUtils
from fastapi import Request, Response
from utils.data_utils import DataUtils
from utils.response_utils import ResponseUtils
from utils.cryptography_utils import CryptographyUtils
from starlette.middleware.base import BaseHTTPMiddleware
from repositories.redis_repository import RedisRepository

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        base = request.url.path[len(request.scope.get("root_path","")):]
        if any(base.startswith(path) for path in Config().PROTECTED_PATHS):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return await ResponseUtils.error(*DataUtils.responses.unauthorized_error)
            try:
                request_token = auth_header.split(" ")[1]
                payload = JWTDTO(**JWTUtils.verify_token(request_token))
                user = await User(login=payload.login).get()
                session = await Session(user_id=user.id).get()
                saved_token = await RedisRepository().get_user(str(user.id))
                if not (session and CryptographyUtils.verify_string(request_token, session.token) 
                        and request_token == saved_token.decode('utf-8')):
                    return await ResponseUtils.error(*DataUtils.responses.unauthenticated_error)
            except Exception as e:
                raise e
        return await call_next(request)