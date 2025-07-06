from DTO import UserDTO
from services import UserService
from fastapi import Request, Response

class UserController:
    async def create_user(request: Request, user: UserDTO) -> Response:
        return await UserService().create_user(request, user)
    
    async def get_user(request: Request, id: int) -> Response:
        return await UserService().get_user(request, id)

    async def delete_user(request: Request, id: int) -> Response:
        return await UserService().delete_user(request, id)