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
        
    async def get_user(self, request: Request, id: int) -> Response:
        existing_user = await UserRepository().get_user(id)

        if existing_user:
            return await ResponseUtils.success(
                DataUtils.responses.user_received_message,
                vars(UserDTO(**vars(existing_user)))
            )
        else:
            return await ResponseUtils.error(request, *DataUtils.responses.user_not_found_error)
        
    async def delete_user(self, request: Request, id: int) -> Response:
        user_repository = UserRepository()
        existing_user = await user_repository.get_user(id)

        if existing_user:
            await user_repository.delete_user(existing_user.id)
            
            return await ResponseUtils.success(DataUtils.responses.user_deleted_message.format(id=id))
        else:
            return await ResponseUtils.error(request, *DataUtils.responses.user_not_found_error)