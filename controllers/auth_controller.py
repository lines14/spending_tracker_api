from DTO import UserDTO
from models import User, Session
from utils.JWT_utils import JWTUtils
from fastapi import Request, Response
from utils.data_utils import DataUtils
from utils.response_utils import ResponseUtils
from utils.cryptography_utils import CryptographyUtils
from repositories.redis_repository import RedisRepository

class AuthController:
    async def auth(self, request: Request, user: UserDTO) -> Response:
        existing_user = await User(login=user.login).get()
        if existing_user and CryptographyUtils.verify_string(user.password, existing_user.hashed_password):
            token = JWTUtils.generate_token(user.login)
            await RedisRepository().set_user(str(existing_user.id), token)
            session = Session(
                user_id=existing_user.id, 
                token=CryptographyUtils.hash_string(token),
                host=request.headers.get('host'),
                user_agent=request.headers.get('user-agent')
            )
            await session.create()
            return await ResponseUtils.success(DataUtils.responses.authorized_message, token)
        else:
            return await ResponseUtils.error(*DataUtils.responses.invalid_credentials_error)