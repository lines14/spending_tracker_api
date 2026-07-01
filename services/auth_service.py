from dto import CredentialsDTO
from exceptions import InvalidCredentialsException
from repositories.session_repository import SessionRepository
from repositories.user_repository import UserRepository
from utils import CryptographyUtils, JWTUtils


class AuthService:
    async def auth(self, headers, credentials: CredentialsDTO) -> str:
        user_repository = UserRepository()
        id = await user_repository.get_user_id_by_login(credentials.login)

        if not id:
            raise InvalidCredentialsException()

        existing_user = await user_repository.get_user(locals())

        if not existing_user or not CryptographyUtils.verify_string(credentials.password, existing_user.hashed_password):
            raise InvalidCredentialsException()

        token = JWTUtils.generate_token(id)
        await SessionRepository().create_session(id, token, headers)

        return token
