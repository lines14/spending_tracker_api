from dto import CredentialsDTO
from fastapi import Request, Response
from repositories.user_repository import UserRepository
from repositories.session_repository import SessionRepository
from utils import JWTUtils, DataUtils, ResponseUtils, CryptographyUtils

class AuthService:
    async def auth(self, request: Request, credentials: CredentialsDTO) -> Response:
        user_repository = UserRepository()
        id = await user_repository.get_user_id_by_login(credentials.login)

        if not id:
            return await ResponseUtils.error(request, *DataUtils.responses.invalid_credentials_error)
        
        existing_user = await user_repository.get_users(locals())

        if existing_user and CryptographyUtils.verify_string(credentials.password, existing_user.hashed_password):
            token = JWTUtils.generate_token(id)

            await SessionRepository().create_session(id, token, request.headers)
            
            return await ResponseUtils.success(DataUtils.responses.authorized_message, token)
        else:
            return await ResponseUtils.error(request, *DataUtils.responses.invalid_credentials_error)