from fastapi import Depends

from dto import CredentialsDTO, UserDTO, UserUpdateDTO
from errors import UserExistsError, UserNotFoundError
from repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.user_repository = user_repository

    async def create_user(self, credentials: CredentialsDTO) -> UserDTO:
        existing_id = await self.user_repository.get_user_id_by_login(credentials.login, with_soft_deleted=True)

        if existing_id:
            raise UserExistsError()

        user = await self.user_repository.create_user(credentials)
        return UserDTO(**user.model_dump())

    async def get_user(self, search_by: dict, with_relations: bool) -> UserDTO:
        user = await self.user_repository.get_user(search_by, with_relations)

        if not user:
            raise UserNotFoundError()

        return UserDTO(**user.model_dump())

    async def get_users(self, search_by: dict, with_relations: bool) -> list[UserDTO]:
        users = await self.user_repository.get_users(search_by, with_relations)
        return [UserDTO(**user.model_dump()) for user in users]

    async def update_user(self, search_by: dict, user: UserUpdateDTO) -> UserDTO:
        existing_user = await self.user_repository.get_user(search_by)

        if not existing_user:
            raise UserNotFoundError()

        if user.login:
            existing_id = await self.user_repository.get_user_id_by_login(user.login, with_soft_deleted=True)

            if existing_id:
                raise UserExistsError()

        updated_user = await self.user_repository.update_user(search_by, user.model_dump(exclude_unset=True))

        return UserDTO(**updated_user.model_dump())

    async def delete_user(self, search_by: dict, soft_delete: bool) -> None:
        user = await self.user_repository.get_user(search_by)

        if not user:
            raise UserNotFoundError()

        await self.user_repository.delete_user(search_by, soft_delete)
