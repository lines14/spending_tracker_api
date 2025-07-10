import json
from models import User
from typing import Optional
from utils import CryptographyUtils
from repositories.base.redis_client import RedisClient
from DTO import RedisSetRequestDTO, CredentialsDTO, UserDTO
from repositories.session_repository import SessionRepository

class UserRepository:    
    async def create_user(self, credentials: CredentialsDTO) -> None:
        redis_client = RedisClient()

        user = User(
            login=credentials.login, 
            hashed_password=CryptographyUtils.hash_string(credentials.password)
        )

        await user.create()
        
        name = redis_client.create_key('user', user.id)
        stringified_user = json.dumps(user.to_dict(), default=str)

        data = RedisSetRequestDTO(
            name=name, 
            value=stringified_user
        )

        await redis_client.set(**data.model_dump())

    async def delete_user(self, id: int) -> None:
        redis_client = RedisClient()
        name = redis_client.create_key('user', id)
        stringified_user = await redis_client.get(name)

        user = UserDTO(**json.loads(stringified_user))

        await SessionRepository().delete_session(id)

        await redis_client.delete(user.login)
        await redis_client.delete(name)

        await User(id=id).delete()
    
    async def get_user(self, id: int) -> Optional[UserDTO]:
        redis_client = RedisClient()
        name = redis_client.create_key('user', id)
        stringified_user = await redis_client.get(name)

        if not stringified_user:
            user = await User(id=id).get()

            if not user:
                return None

            stringified_user = json.dumps(user.to_dict(), default=str)

            data = RedisSetRequestDTO(
                name=name, 
                value=stringified_user
            )

            await redis_client.set(**data.model_dump())

        return UserDTO(**json.loads(stringified_user))
    
    async def get_user_id_by_login(self, login: str) -> Optional[int]:
        redis_client = RedisClient()
        user_id = await redis_client.get(login)

        if not user_id:
            user = await User(login=login).get()

            if not user:
                return None

            user_id = str(user.id)

            data = RedisSetRequestDTO(
                name=user.login,
                value=user_id
            )

            await redis_client.set(**data.model_dump())

        return int(user_id)
    
    async def get_user_with_relations(self, id: int) -> Optional[UserDTO]:
        redis_client = RedisClient()
        name = redis_client.create_key('user_with_relations', id)
        stringified_user = await redis_client.get(name)

        if not stringified_user:
            user = await User(id=id).joined_load(["bank_accounts", "bank_accounts.purchases"])

            if not user:
                return None

            stringified_user = json.dumps(User.nested_models_to_dict(user), default=str)

            data = RedisSetRequestDTO(
                name=name, 
                value=stringified_user
            )

            await redis_client.set(**data.model_dump())

        return UserDTO(**json.loads(stringified_user))