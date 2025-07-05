from DTO import UserDTO
from models import User
from fastapi import Response
from utils.data_utils import DataUtils
from utils.response_utils import ResponseUtils
from utils.cryptography_utils import CryptographyUtils

class RegistrationHandler:
    async def registration(self, user: UserDTO) -> Response:
        existing_user = await User(login=user.login).get()
        if not existing_user:
            new_user = User(
                login=user.login, 
                hashed_password=CryptographyUtils.hash_string(user.password)
            )
            await new_user.create()
            return await ResponseUtils.success(DataUtils.responses.registered_message)
        else:
            return await ResponseUtils.error(*DataUtils.responses.user_exists_error)