from DTO import UserDTO
from services import AuthService
from fastapi import Request, Response

class AuthController:
    async def auth(request: Request, user: UserDTO) -> Response:
        return await AuthService().auth(request, user)