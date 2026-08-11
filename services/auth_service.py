from fastapi import Depends

from dto import CredentialsDTO
from errors import InvalidCredentialsError
from repositories.session_repository import SessionRepository
from repositories.user_repository import UserRepository
from utils import CryptographyUtils, JWTUtils


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        session_repository: SessionRepository = Depends(),
    ):
        self.user_repository = user_repository
        self.session_repository = session_repository

    async def auth(self, headers, credentials: CredentialsDTO) -> str:
        id = await self.user_repository.get_user_id_by_login(credentials.login)

        if not id:
            raise InvalidCredentialsError()

        existing_user = await self.user_repository.get_user(locals())

        if not existing_user or not CryptographyUtils.verify_string(
            credentials.password, existing_user.hashed_password
        ):
            raise InvalidCredentialsError()

        token = JWTUtils.generate_token(id)
        await self.session_repository.create_session(id, token, headers)

        return token
