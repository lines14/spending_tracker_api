from fastapi import Depends, Request, Response

from dto import CredentialsDTO
from services import AuthService
from utils import DataUtils, ResponseUtils


class AuthController:
    async def auth(
        request: Request,
        credentials: CredentialsDTO,
        service: AuthService = Depends()
    ) -> Response:
        token = await service.auth(request.headers, credentials)
        return await ResponseUtils.success(DataUtils.responses.authorized_message, token)
