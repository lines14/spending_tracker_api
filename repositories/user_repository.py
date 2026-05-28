import json
from os import getenv
from models import User
from typing import Optional
from utils import CryptographyUtils, DataUtils
from repositories.base.cache_tagger import CacheTagger
from repositories.base.redis_client import RedisClient
from repositories.base.base_repository import BaseRepository
from repositories.session_repository import SessionRepository
from dto import RedisSetRequestDTO, RedisSetexWithTagsRequestDTO, CredentialsDTO, UserDTO

class UserRepository(BaseRepository):    
    def __init__(self):
        super().__init__(model=User)

    async def create_user(self, credentials: CredentialsDTO) -> UserDTO:
        user = self.model(
            login=credentials.login, 
            hashed_password=CryptographyUtils.hash_string(credentials.password)
        )

        await self.create(user)
        
        stringified_user = json.dumps(user.model_dump(), default=str)

        return UserDTO(**json.loads(stringified_user))

    async def delete_user(self, search_by: dict, soft_delete: bool) -> None:
        search_by = DataUtils.filter_search_fields(search_by, self.model)

        if 'id' in search_by:
            id = DataUtils.dict_to_model(search_by).id

            async def delete_from_cache(id):
                redis_client = RedisClient()
                key = redis_client.create_key('user', id)
                stringified_user = await redis_client.get(key)

                user = UserDTO(**json.loads(stringified_user))
                
                await SessionRepository().delete_session(id)

                await redis_client.delete(user.login)
                await redis_client.delete(key)

            if isinstance(id, list) and len(id) > 0:
                for element in id:
                    await delete_from_cache(element)
            else:
                await delete_from_cache(id)

        await self.delete(soft_delete, search_by)

    async def update_user(
        self, 
        search_by: dict, 
        user: dict
    ) -> Optional[UserDTO]:
        redis_client = RedisClient()

        search_by = DataUtils.filter_search_fields(search_by, self.model)

        if 'password' in user:
            password = user['password']
            user['hashed_password'] = CryptographyUtils.hash_string(password)
            del user['password']

        result = await self.update_one(search_by, user)

        if not result:
            return None
        
        stringified_user = json.dumps(result.model_dump(), default=str)
        key = redis_client.create_key('user', result.id)
        await redis_client.delete(key)

        return UserDTO(**json.loads(stringified_user))
    
    async def get_user_id_by_login(self, login: str) -> Optional[int]:
        redis_client = RedisClient()
        user_id = await redis_client.get(login)

        if not user_id:
            result = await self.get_one_or_none({"login": login})

            if not result:
                return None

            user_id = str(result.id)

            data = RedisSetRequestDTO(
                name=result.login,
                value=user_id
            )

            await redis_client.set(**data.model_dump())

        return int(user_id)

    async def get_users(
        self, 
        search_by: dict, 
        with_soft_deleted: bool = False
    ) -> list[UserDTO]:
        stringified_users_list = []
        redis_client = RedisClient()

        search_by = DataUtils.filter_search_fields(search_by, self.model)

        if 'id' in search_by:
            uncached_ids = []
            ids = search_by['id'] if isinstance(search_by['id'], list) else [search_by['id']]

            for user_id in ids:
                key = redis_client.create_key('user', user_id)
                cached_user = await redis_client.get(key)

                if cached_user:
                    stringified_users_list.append(cached_user)
                else:
                    uncached_ids.append(user_id)

            if uncached_ids:
                result = await self.get_all({"id": uncached_ids}, with_soft_deleted)

                if result:
                    for user in result:
                        stringified_user = json.dumps(user.model_dump(), default=str)
                        stringified_users_list.append(stringified_user)
                        key = redis_client.create_key('user', user.id)

                        data = RedisSetRequestDTO(
                            name=key, 
                            value=stringified_user
                        )

                        await redis_client.set(**data.model_dump())

            if not stringified_users_list:
                return []

            return [UserDTO(**json.loads(user)) for user in stringified_users_list]

        else:
            result = await self.get_all(search_by, with_soft_deleted)
            if not result:
                return []

            return [UserDTO.model_validate(user) for user in result]


    async def get_user(
        self, 
        search_by: dict, 
        with_soft_deleted: bool = False
    ) -> Optional[UserDTO]:
        redis_client = RedisClient()

        search_by = DataUtils.filter_search_fields(search_by, self.model)

        if 'id' in search_by:
            key = redis_client.create_key('user', DataUtils.dict_to_model(search_by).id)
            stringified_user = await redis_client.get(key)

            if not stringified_user:
                result = await self.get_one_or_none(search_by, with_soft_deleted)

                if not result:
                    return None

                stringified_user = json.dumps(result.model_dump(), default=str)

                data = RedisSetRequestDTO(
                    name=key, 
                    value=stringified_user
                )

                await redis_client.set(**data.model_dump())
            
            return UserDTO(**json.loads(stringified_user))

        else:
            result = await self.get_one_or_none(search_by, with_soft_deleted)

            if not result:
                return None
            
            stringified_user = json.dumps(result.model_dump(), default=str)
            
            return UserDTO(**json.loads(stringified_user))

    async def get_users_with_relations(
        self, 
        search_by: dict,
        with_soft_deleted: bool = False
    ) -> list[UserDTO]:
        stringified_users_list = []
        redis_client = RedisClient()
        relations = ["bank_accounts", "bank_accounts.purchases"]

        search_by = DataUtils.filter_search_fields(search_by, self.model)

        if 'id' in search_by:
            uncached_ids = []
            ids = search_by['id'] if isinstance(search_by['id'], list) else [search_by['id']]

            for user_id in ids:
                key = redis_client.create_key('user_with_relations', user_id)
                cached_user = await redis_client.get(key)

                if cached_user:
                    stringified_users_list.append(cached_user)
                else:
                    uncached_ids.append(user_id)

            if uncached_ids:
                result = await self.get_all_with_joinedload(
                    {"id": uncached_ids}, 
                    relations, 
                    with_soft_deleted
                )

                if result:
                    for user in result:
                        user_dict = self.model.nested_models_to_dict(user)
                        clean_dict = json.loads(json.dumps(user_dict, default=str))
                        stringified_user = json.dumps(user_dict, default=str)
                        stringified_users_list.append(stringified_user)
                        key = redis_client.create_key('user_with_relations', user.id)
                        dynamic_tags = CacheTagger.extract_tags_from_dto(UserDTO(**clean_dict))

                        data = RedisSetexWithTagsRequestDTO(
                            name=key,
                            time=getenv('USER_TTL'),
                            value=stringified_user,
                            tags=dynamic_tags,
                        )

                        await redis_client.setex_with_tags(**data.model_dump())

            if not stringified_users_list:
                return []

            return [UserDTO(**json.loads(user)) for user in stringified_users_list]

        else:
            result = await self.get_all_with_joinedload(
                search_by, 
                relations, 
                with_soft_deleted
            )
            
            if not result:
                return []

            return [UserDTO(**self.model.nested_models_to_dict(user)) for user in result]


    async def get_user_with_relations(
        self, 
        search_by: dict,
        with_soft_deleted: bool = False
    ) -> Optional[UserDTO]:
        redis_client = RedisClient()
        relations = ["bank_accounts", "bank_accounts.purchases"]

        search_by = DataUtils.filter_search_fields(search_by, self.model)

        if 'id' in search_by:
            key = redis_client.create_key('user_with_relations', DataUtils.dict_to_model(search_by).id)
            stringified_user = await redis_client.get(key)

            if not stringified_user:
                result = await self.get_one_or_none_with_joinedload(
                    search_by, 
                    relations, 
                    with_soft_deleted
                )

                if not result:
                    return None

                user_dict = self.model.nested_models_to_dict(result)
                clean_dict = json.loads(json.dumps(user_dict, default=str))
                stringified_user = json.dumps(user_dict, default=str)
                dynamic_tags = CacheTagger.extract_tags_from_dto(UserDTO(**clean_dict))

                data = RedisSetexWithTagsRequestDTO(
                    name=key,
                    time=getenv('USER_TTL'),
                    value=stringified_user,
                    tags=dynamic_tags,
                )

                await redis_client.setex_with_tags(**data.model_dump())
            
            return UserDTO(**json.loads(stringified_user))

        else:
            result = await self.get_one_or_none_with_joinedload(
                search_by, 
                relations, 
                with_soft_deleted
            )

            if not result:
                return None
            
            stringified_user = json.dumps(self.model.nested_models_to_dict(result), default=str)
            
            return UserDTO(**json.loads(stringified_user))