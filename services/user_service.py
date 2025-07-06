from DTO import UserDTO
from models import User
from fastapi import Response, Request
from utils import DataUtils, ResponseUtils, CryptographyUtils

class UserService:
    async def create_user(self, request: Request, user: UserDTO) -> Response:
        existing_user = await User(login=user.login).get()

        if not existing_user:
            new_user = User(
                login=user.login, 
                hashed_password=CryptographyUtils.hash_string(user.password)
            )
            await new_user.create()

            return await ResponseUtils.success(DataUtils.responses.user_created_message)
        else:
            return await ResponseUtils.error(request, *DataUtils.responses.user_exists_error)
        
    async def delete_user(self, request: Request, id: int) -> Response:
        existing_user = await User(id=id).get()

        if existing_user:
            await User(id=existing_user.id).delete()
            
            return await ResponseUtils.success(DataUtils.responses.user_deleted_message.format(id=id))
        else:
            return await ResponseUtils.error(request, *DataUtils.responses.user_not_found_error)