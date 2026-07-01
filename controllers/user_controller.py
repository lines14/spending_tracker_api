from typing import Annotated

from fastapi import Body, Depends, Path, Query, Request, Response

from dto import CredentialsDTO, UserUpdateDTO
from services import UserService
from utils import DataUtils, ResponseUtils


class UserController:
    async def create_user(
        request: Request,
        credentials: CredentialsDTO,
        service: UserService = Depends()
    ) -> Response:
        user = await service.create_user(credentials)

        return await ResponseUtils.success(
            DataUtils.responses.user_created_message,
            user.model_dump()
        )

    async def get_user(
        request: Request,
        id: int,
        with_relations: bool | None = False,
        service: UserService = Depends()
    ) -> Response:
        user = await service.get_user(locals(), with_relations)

        return await ResponseUtils.success(
            DataUtils.responses.user_received_message,
            user.model_dump()
        )

    async def get_users(
        id: list[int] | None = Query(None, alias="ids"),
        with_relations: bool | None = False,
        service: UserService = Depends()
    ) -> Response:
        users = await service.get_users(locals(), with_relations)

        return await ResponseUtils.success(
            DataUtils.responses.users_received_message,
            [user.model_dump() for user in users]
        )

    async def update_user(
        request: Request,
        user: Annotated[UserUpdateDTO, Body(...)],
        id: int = Path(...),
        service: UserService = Depends()
    ) -> Response:
        updated_user = await service.update_user(locals(), user)

        return await ResponseUtils.success(
            DataUtils.responses.user_updated_message.format(id=id),
            updated_user.model_dump()
        )

    async def delete_user(
        request: Request,
        id: int,
        soft_delete: bool | None = True,
        service: UserService = Depends()
    ) -> Response:
        await service.delete_user(locals(), soft_delete)

        return await ResponseUtils.success(
            DataUtils.responses.user_deleted_message.format(id=id)
        )
