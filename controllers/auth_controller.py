from DTO import CredentialsDTO
from services import AuthService
from fastapi import Request, Response

class AuthController:
    async def auth(request: Request, credentials: CredentialsDTO) -> Response:
        return await AuthService().auth(request, credentials)