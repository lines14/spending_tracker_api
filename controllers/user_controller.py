from typing import Optional
from typing import Annotated
from services import UserService
from DTO import CredentialsDTO, UserUpdateDTO
from fastapi import Request, Response, Path, Body

class UserController:
    async def create_user(request: Request, credentials: CredentialsDTO) -> Response:
        return await UserService().create_user(request, credentials)
    
    async def get_user(request: Request, id: int, with_relations: Optional[bool] = False) -> Response:
        return await UserService().get_user(request, locals(), with_relations)
    
    async def update_user(request: Request, user: Annotated[UserUpdateDTO, Body(...)], id: int = Path(...)) -> Response:
        return await UserService().update_user(request, id, user)

    async def delete_user(request: Request, id: int, soft_delete: Optional[bool] = True) -> Response:
        return await UserService().delete_user(request, locals(), soft_delete)