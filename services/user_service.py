from fastapi import Response, Request
from utils import DataUtils, ResponseUtils
from dto import CredentialsDTO, UserDTO, UserUpdateDTO
from repositories.user_repository import UserRepository

class UserService:
    async def create_user(self, request: Request, credentials: CredentialsDTO) -> Response:
        user_repository = UserRepository()

        existing_id = await user_repository.get_user_id_by_login(credentials.login)

        if not existing_id:
            created_user = await user_repository.create_user(credentials)

            return await ResponseUtils.success(
                DataUtils.responses.user_created_message,
                UserDTO(**created_user.model_dump()).model_dump()
            )
        else:
            return await ResponseUtils.error(request, *DataUtils.responses.user_exists_error)
        
    async def get_user(self, request: Request, search_by: dict, with_relations: bool) -> Response:
        user_repository = UserRepository()

        existing_user = (await user_repository.get_user_with_relations(search_by) 
                         if with_relations else await user_repository.get_user(search_by))

        if not existing_user:
            return await ResponseUtils.error(request, *DataUtils.responses.user_not_found_error)

        return await ResponseUtils.success(
            DataUtils.responses.user_received_message,
            UserDTO(**existing_user.model_dump()).model_dump()
        )

    async def update_user(self, request: Request, search_by: dict, user: UserUpdateDTO) -> Response:
        user_repository = UserRepository()

        existing_user = await user_repository.get_user(search_by, with_soft_deleted=True)

        if not existing_user:
            return await ResponseUtils.error(request, *DataUtils.responses.user_not_found_error)

        updated_user = await user_repository.update_user(
            search_by, 
            user.model_dump(exclude_unset=True)
        )

        return await ResponseUtils.success(
            DataUtils.responses.user_updated_message.format(id=DataUtils.dict_to_model(search_by).id),
            UserDTO(**updated_user.model_dump()).model_dump()
        )

    async def delete_user(self, request: Request, search_by: dict, soft_delete: bool) -> Response:
        user_repository = UserRepository()

        existing_user = await user_repository.get_user(search_by)

        if existing_user:
            await user_repository.delete_user(search_by, soft_delete)
            
            return await ResponseUtils.success(
                DataUtils.responses.user_deleted_message.format(id=DataUtils.dict_to_model(search_by).id)
            )
        else:
            return await ResponseUtils.error(request, *DataUtils.responses.user_not_found_error)