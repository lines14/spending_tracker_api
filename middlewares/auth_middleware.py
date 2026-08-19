from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from config import Config
from dto import JWTDTO
from repositories.session_repository import SessionRepository
from utils import CryptographyUtils, DataUtils, JWTUtils, ResponseUtils


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        base = request.url.path[len(request.scope.get("root_path", "")) :]

        if any(base.startswith(path) for path in Config().protected_paths):
            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                return await ResponseUtils.error(request, *DataUtils.responses.unauthorized_error)

            try:
                request_token = auth_header.split(" ")[1]
                payload = JWTDTO(**JWTUtils.verify_token(request_token))
                session = await SessionRepository().get_session(payload.id)

                if not session:
                    return await ResponseUtils.error(request, *DataUtils.responses.session_expired_error)

                if not CryptographyUtils.verify_fingerprint(request_token, session.token_fingerprint):
                    return await ResponseUtils.error(request, *DataUtils.responses.unauthenticated_error)
            except Exception as e:
                raise e

        return await call_next(request)
