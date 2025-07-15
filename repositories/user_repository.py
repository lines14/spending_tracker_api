import json
from typing import Optional
from models import User, BankAccount
from utils import CryptographyUtils, DataUtils
from repositories.base.redis_client import RedisClient
from repositories.session_repository import SessionRepository
from DTO import RedisSetRequestDTO, CredentialsDTO, UserDTO, UserUpdateDTO

class UserRepository:    
    async def create_user(self, credentials: CredentialsDTO) -> None:
        redis_client = RedisClient()

        new_user = User(
            login=credentials.login, 
            hashed_password=CryptographyUtils.hash_string(credentials.password)
        )

        await new_user.create()
        
        name = redis_client.create_key('user', new_user.id)
        new_stringified_user = json.dumps(new_user.to_dict(), default=str)

        data = RedisSetRequestDTO(
            name=name, 
            value=new_stringified_user
        )

        await redis_client.set(**data.model_dump())

    async def delete_users(self, search_by: dict, soft_delete: bool) -> None:
        if 'id' in search_by:
            id = DataUtils.dict_to_model(search_by).id

            redis_client = RedisClient()
            name = redis_client.create_key('user', id)
            stringified_user = await redis_client.get(name)

            user = UserDTO(**json.loads(stringified_user))
            
            await SessionRepository().delete_session(id)

            await redis_client.delete(user.login)
            await redis_client.delete(name)

        await User(**search_by).delete(soft_delete)
    
    async def update_users(self, user: UserUpdateDTO) -> Optional[UserDTO]:
        if user.password:
            user.hashed_password = CryptographyUtils.hash_string(user.password)
            delattr(user, 'password')
            
        result = await User(**user.model_dump(exclude_unset=True)).update()

        if not result:
            return None
        
        for user in result:
            stringified_user = json.dumps(user.to_dict(), default=str)

            if hasattr(user, 'id'):
                redis_client = RedisClient()
                name = redis_client.create_key('user', user.id)

                data = RedisSetRequestDTO(
                    name=name, 
                    value=stringified_user
                )

                await redis_client.set(**data.model_dump())

        return [UserDTO(**item) for item in json.loads(stringified_user)] if len(result) > 1 else UserDTO(**json.loads(stringified_user))
    
    async def get_users(self, search_by: dict, with_soft_deleted: bool = False) -> Optional[UserDTO]:
        stringified_user= None

        if 'id' in search_by:
            redis_client = RedisClient()
            name = redis_client.create_key('user', DataUtils.dict_to_model(search_by).id)
            stringified_user = await redis_client.get(name)

        if not stringified_user:
            print(search_by)
            result = await User(**search_by).get(with_soft_deleted)

            if not result:
                return None
            
            user = result.pop()
            stringified_user = json.dumps(user.to_dict(), default=str)

            if 'id' in search_by:
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
            result = await User(login=login).get()

            if not result:
                return None

            user = result.pop()
            user_id = str(user.id)

            data = RedisSetRequestDTO(
                name=user.login,
                value=user_id
            )

            await redis_client.set(**data.model_dump())

        return int(user_id)
    
    async def get_users_with_relations(self, search_by: dict) -> Optional[UserDTO]:
        stringified_user= None

        if 'id' in search_by:
            redis_client = RedisClient()
            name = redis_client.create_key('user_with_relations', DataUtils.dict_to_model(search_by).id)
            stringified_user = await redis_client.get(name)

        if not stringified_user:
            result = await User(**search_by).joined_load(["bank_accounts", "bank_accounts.purchases"])

            if not result:
                return None

            user = result.pop()
            stringified_user = json.dumps(User.nested_models_to_dict(user), default=str)

            if 'id' in search_by:
                data = RedisSetRequestDTO(
                    name=name, 
                    value=stringified_user
                )

                await redis_client.set(**data.model_dump())

        return UserDTO(**json.loads(stringified_user))