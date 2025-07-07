from DTO import CredentialsDTO
from fastapi import Request, Response
from repositories.user_repository import UserRepository
from repositories.session_repository import SessionRepository
from utils import JWTUtils, DataUtils, ResponseUtils, CryptographyUtils

class AuthService:
    async def auth(self, request: Request, credentials: CredentialsDTO) -> Response:
        user_repository = UserRepository()
        existing_id = await user_repository.get_user_id_by_login(credentials.login)

        if not existing_id:
            return await ResponseUtils.error(request, *DataUtils.responses.invalid_credentials_error)
        
        existing_user = await user_repository.get_user(existing_id)

        if existing_user and CryptographyUtils.verify_string(credentials.password, existing_user.hashed_password):
            token = JWTUtils.generate_token(existing_id)

            await SessionRepository().create_session(existing_id, token, request.headers)
            
            return await ResponseUtils.success(DataUtils.responses.authorized_message, token)
        else:
            return await ResponseUtils.error(request, *DataUtils.responses.invalid_credentials_error)