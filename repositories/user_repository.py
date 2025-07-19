import json
from models import User
from typing import Optional, Union
from utils import CryptographyUtils, DataUtils
from repositories.base.redis_client import RedisClient
from DTO import RedisSetRequestDTO, CredentialsDTO, UserDTO
from repositories.session_repository import SessionRepository

class UserRepository:    
    async def create_user(self, credentials: CredentialsDTO) -> UserDTO:
        redis_client = RedisClient()

        new_user = User(
            login=credentials.login, 
            hashed_password=CryptographyUtils.hash_string(credentials.password)
        )

        await new_user.create()
        
        name = redis_client.create_key('user', new_user.id)
        new_stringified_user = json.dumps(new_user.model_dump(), default=str)

        data = RedisSetRequestDTO(
            name=name, 
            value=new_stringified_user
        )

        await redis_client.set(**data.model_dump())

        return UserDTO(**json.loads(new_stringified_user))

    async def delete_users(self, search_by: dict, soft_delete: bool) -> None:
        if 'id' in search_by:
            id = DataUtils.dict_to_model(search_by).id

            async def delete_from_cache(id):
                redis_client = RedisClient()
                name = redis_client.create_key('user', id)
                stringified_user = await redis_client.get(name)

                user = UserDTO(**json.loads(stringified_user))
                
                await SessionRepository().delete_session(id)

                await redis_client.delete(user.login)
                await redis_client.delete(name)

            if isinstance(id, list) and len(id) > 0:
                for element in id:
                    await delete_from_cache(element)
            else:
                await delete_from_cache(id)

        await User.delete(search_by, soft_delete)

    async def update_users(
        self, 
        search_by: dict, 
        user: dict
    ) -> Optional[Union[UserDTO, list[UserDTO]]]:
        updated_users = []
        redis_client = RedisClient()

        if 'password' in user:
            password = user['password']

            if isinstance(password, list):
                user['hashed_password'] = [CryptographyUtils.hash_string(element) 
                                           for element in password]
            else:
                user['hashed_password'] = CryptographyUtils.hash_string(password)

            del user['password']

        result = await User.update(search_by, user)

        if not result:
            return None

        for user in result:
            stringified_user = json.dumps(user.model_dump(), default=str)
            updated_users.append(stringified_user)

            if hasattr(user, 'id'):
                name = redis_client.create_key('user', user.id)

                data = RedisSetRequestDTO(
                    name=name,
                    value=stringified_user
                )

                await redis_client.set(**data.model_dump())

        return [UserDTO(**json.loads(user)) for user in updated_users] if len(updated_users) > 1 \
            else UserDTO(**json.loads(updated_users[0]))


    async def get_users(
        self, 
        search_by: dict, 
        with_soft_deleted: bool = False
    ) -> Optional[Union[UserDTO, list[UserDTO]]]:
        stringified_users_list = []
        redis_client = RedisClient()

        if 'id' in search_by:
            uncached_ids = []

            ids = search_by['id'] if isinstance(search_by['id'], list) else [search_by['id']]

            for user_id in ids:
                name = redis_client.create_key('user', user_id)
                cached_user = await redis_client.get(name)

                if cached_user:
                    stringified_users_list.append(cached_user)
                else:
                    uncached_ids.append(user_id)

            if uncached_ids:
                result = await User.get({"id": uncached_ids}, with_soft_deleted)

                if not result:
                    return None
                
                for user in result:
                    stringified_user = json.dumps(user.model_dump(), default=str)
                    stringified_users_list.append(stringified_user)
                    name = redis_client.create_key('user', user.id)

                    data = RedisSetRequestDTO(
                        name=name, 
                        value=stringified_user
                    )

                    await redis_client.set(**data.model_dump())

            return [UserDTO(**json.loads(stringified_user)) for stringified_user 
                    in stringified_users_list] if len(ids) > 1 \
                        else UserDTO(**json.loads(stringified_users_list[0]))

        else:
            result = await User.get(search_by, with_soft_deleted)

            if not result:
                return None

            return [UserDTO(**json.loads(json.dumps(user.model_dump(), default=str))) 
                    for user in result] if len(result) > 1 \
                        else UserDTO(**json.loads(json.dumps(result[0].model_dump(), default=str)))
    
    async def get_user_id_by_login(self, login: str) -> Optional[int]:
        redis_client = RedisClient()
        user_id = await redis_client.get(login)

        if not user_id:
            result = await User(login=login).validated_get()

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

    async def get_users_with_relations(
        self, 
        search_by: dict
    ) -> Optional[Union[UserDTO, list[UserDTO]]]:
        stringified_users_list = []
        redis_client = RedisClient()

        if 'id' in search_by:
            uncached_ids = []
            ids = search_by['id'] if isinstance(search_by['id'], list) else [search_by['id']]

            for user_id in ids:
                name = redis_client.create_key('user_with_relations', user_id)
                cached_user = await redis_client.get(name)

                if cached_user:
                    stringified_users_list.append(cached_user)
                else:
                    uncached_ids.append(user_id)

            if uncached_ids:
                result = await User.get_with_joined_load(
                    {"id": uncached_ids}, 
                    ["bank_accounts", "bank_accounts.purchases"]
                )

                for user in result:
                    stringified_user = json.dumps(User.nested_models_to_dict(user), default=str)
                    stringified_users_list.append(stringified_user)
                    name = redis_client.create_key('user_with_relations', user.id)

                    data = RedisSetRequestDTO(
                        name=name, 
                        value=stringified_user
                    )

                    await redis_client.set(**data.model_dump())

            return [UserDTO(**json.loads(stringified_user)) for stringified_user 
                    in stringified_users_list] if len(ids) > 1 \
                        else UserDTO(**json.loads(stringified_users_list[0]))

        else:
            result = await User.get_with_joined_load(
                search_by, 
                ["bank_accounts", "bank_accounts.purchases"]
            )

            if not result:
                return None

            return [UserDTO(**json.loads(json.dumps(User.nested_models_to_dict(user), default=str))) 
                    for user in result] if len(result) > 1 \
                        else UserDTO(**json.loads(json.dumps(User.nested_models_to_dict(result[0]), default=str)))