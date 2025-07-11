from fastapi import Response, Request
from DTO import CredentialsDTO, UserDTO
from utils import DataUtils, ResponseUtils
from repositories.user_repository import UserRepository

class UserService:
    async def create_user(self, request: Request, credentials: CredentialsDTO) -> Response:
        user_repository = UserRepository()
        existing_id = await user_repository.get_user_id_by_login(credentials.login)

        if not existing_id:
            await user_repository.create_user(credentials)

            return await ResponseUtils.success(DataUtils.responses.user_created_message)
        else:
            return await ResponseUtils.error(request, *DataUtils.responses.user_exists_error)
        
    async def get_user(self, request: Request, id: int, with_relations: bool) -> Response:
        user_repository = UserRepository()
        existing_user = (await user_repository.get_user_with_relations(id) 
                         if with_relations else await user_repository.get_user(id))

        if not existing_user:
            return await ResponseUtils.error(request, *DataUtils.responses.user_not_found_error)

        return await ResponseUtils.success(
            DataUtils.responses.user_received_message,
            UserDTO(**existing_user.model_dump()).model_dump()
        )
        
    async def delete_user(self, request: Request, id: int, soft_delete: bool) -> Response:
        user_repository = UserRepository()
        existing_user = await user_repository.get_user(id)

        if existing_user:
            await user_repository.delete_user(existing_user.id, soft_delete)
            
            return await ResponseUtils.success(DataUtils.responses.user_deleted_message.format(id=id))
        else:
            return await ResponseUtils.error(request, *DataUtils.responses.user_not_found_error)