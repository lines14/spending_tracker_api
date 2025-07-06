from DTO import UserDTO
from services import AuthService
from fastapi import Request, Response

class AuthController:
    async def auth(request: Request, user: UserDTO) -> Response:
        auth_service = AuthService()
        return await auth_service.auth(request, user)