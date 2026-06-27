from fastapi import Query
from typing import Optional
from typing import Annotated
from services import UserService
from dto import CredentialsDTO, UserUpdateDTO
from fastapi import Request, Response, Path, Body, Depends

class UserController:
    async def create_user(
        request: Request, 
        credentials: CredentialsDTO,
        service: UserService = Depends()
    ) -> Response:
        return await service.create_user(request, credentials)
    
    async def get_user(
        request: Request, 
        id: int, 
        with_relations: Optional[bool] = False,
        service: UserService = Depends()
    ) -> Response:
        return await service.get_user(request, locals(), with_relations)
    
    async def get_users(
        id: Optional[list[int]] = Query(None, alias="ids"),
        with_relations: Optional[bool] = False,
        service: UserService = Depends()
    ) -> Response:
        return await service.get_users(locals(), with_relations)
    
    async def update_user(
        request: Request, 
        user: Annotated[UserUpdateDTO, Body(...)], 
        id: int = Path(...),
        service: UserService = Depends()
    ) -> Response:
        return await service.update_user(request, locals(), user)

    async def delete_user(
        request: Request, 
        id: int, 
        soft_delete: Optional[bool] = True,
        service: UserService = Depends()
    ) -> Response:
        return await service.delete_user(request, locals(), soft_delete)