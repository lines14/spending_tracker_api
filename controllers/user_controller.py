from DTO import UserDTO
from services import UserService
from fastapi import Request, Response

class UserController:
    async def create_user(request: Request, user: UserDTO) -> Response:
        user_service = UserService()
        return await user_service.create_user(request, user)

    async def delete_user(request: Request, id: int) -> Response:
        user_service = UserService()
        return await user_service.delete_user(request, id)