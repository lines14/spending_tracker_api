from typing import Annotated

from fastapi import Body, Depends, Path, Query, Response

from dto import CredentialsDTO, UserUpdateDTO
from services import UserService
from utils import DataUtils, ResponseUtils


class UserController:
    @staticmethod
    async def create_user(credentials: CredentialsDTO, user_service: UserService = Depends()) -> Response:
        user = await user_service.create_user(credentials)

        return await ResponseUtils.success(DataUtils.responses.user_created_message, user.model_dump())

    @staticmethod
    async def get_user(id: int, with_relations: bool | None = False, user_service: UserService = Depends()) -> Response:
        user = await user_service.get_user(locals(), with_relations)

        return await ResponseUtils.success(DataUtils.responses.user_received_message, user.model_dump())

    @staticmethod
    async def get_users(
        id: list[int] | None = Query(None, alias="ids"),
        with_relations: bool | None = False,
        user_service: UserService = Depends(),
    ) -> Response:
        users = await user_service.get_users(locals(), with_relations)

        return await ResponseUtils.success(
            DataUtils.responses.users_received_message, [user.model_dump() for user in users]
        )

    @staticmethod
    async def update_user(
        user: Annotated[UserUpdateDTO, Body(...)], id: int = Path(...), user_service: UserService = Depends()
    ) -> Response:
        updated_user = await user_service.update_user(locals(), user)

        return await ResponseUtils.success(
            DataUtils.responses.user_updated_message.format(id=id), updated_user.model_dump()
        )

    @staticmethod
    async def delete_user(id: int, soft_delete: bool | None = True, user_service: UserService = Depends()) -> Response:
        await user_service.delete_user(locals(), soft_delete)

        return await ResponseUtils.success(DataUtils.responses.user_deleted_message.format(id=id))
