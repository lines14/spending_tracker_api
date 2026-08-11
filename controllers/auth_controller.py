from fastapi import Depends, Request, Response

from dto import CredentialsDTO
from services import AuthService
from utils import DataUtils, ResponseUtils


class AuthController:
    @staticmethod
    async def auth(request: Request, credentials: CredentialsDTO, auth_service: AuthService = Depends()) -> Response:
        token = await auth_service.auth(request.headers, credentials)
        return await ResponseUtils.success(DataUtils.responses.authorized_message, token)
