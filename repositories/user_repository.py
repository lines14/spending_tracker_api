import json
from os import getenv
from models import User
from typing import Optional
from utils import CacheUtils
from utils import CryptographyUtils, DataUtils
from repositories.base.redis_client import RedisClient
from repositories.base.base_repository import BaseRepository
from dto import RedisSetexRequestDTO, RedisSetexWithTagsRequestDTO, CredentialsDTO, UserDTO

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
        await self.delete(soft_delete, search_by)

    async def update_user(
        self, 
        search_by: dict, 
        user: dict
    ) -> Optional[UserDTO]:
        search_by = DataUtils.filter_search_fields(search_by, self.model)

        if 'password' in user:
            password = user['password']
            user['hashed_password'] = CryptographyUtils.hash_string(password)
            del user['password']

        result = await self.update_one(search_by, user)

        if not result:
            return None
        
        stringified_user = json.dumps(result.model_dump(), default=str)

        return UserDTO(**json.loads(stringified_user))
    
    async def get_user_id_by_login(self, login: str) -> Optional[int]:
        redis_client = RedisClient()
        id = await redis_client.get(login)

        if not id:
            result = await self.get_one_or_none({"login": login})

            if not result:
                return None

            id = str(result.id)

            data = RedisSetexRequestDTO(
                name=result.login,
                time=getenv('USER_TTL'),
                value=id
            )

            await redis_client.setex(**data.model_dump())

        return int(id)
    
    async def get_user(
        self, 
        search_by: dict,
        with_relations: bool = False,
        with_soft_deleted: bool = False
    ) -> Optional[UserDTO]:
        relations = []
        redis_client = RedisClient()
        
        if with_relations:
            relations = self.get_relations()

        search_by = DataUtils.filter_search_fields(search_by, self.model)
        
        prefix = 'user_with_relations' if with_relations else 'user'
        key = redis_client.create_key(prefix, DataUtils.dict_to_model(search_by).id)
        stringified_user = None if with_soft_deleted else await redis_client.get(key)

        if not stringified_user:
            result = (
                await self.get_one_or_none_with_joinedload(search_by, relations, with_soft_deleted) 
                if with_relations else 
                await self.get_one_or_none(search_by, with_soft_deleted)
            )

            if not result:
                return None

            user_dict = self.model.nested_models_to_dict(result)
            clean_dict = json.loads(json.dumps(user_dict, default=str))
            stringified_user = json.dumps(user_dict, default=str)
            tags = CacheUtils.extract_cache_tags_from_dto(UserDTO(**clean_dict))

            data = RedisSetexWithTagsRequestDTO(
                name=key,
                time=getenv('USER_TTL'),
                value=stringified_user,
                tags=tags,
            )

            if not with_soft_deleted:
                await redis_client.setex_with_tags(**data.model_dump())
        
        return UserDTO(**json.loads(stringified_user))

    async def get_users(
        self, 
        search_by: dict,
        with_relations: bool,
        with_soft_deleted: bool = False
    ) -> list[UserDTO]:
        relations = []
        stringified_users_list = []
        redis_client = RedisClient()
        
        if with_relations:
            relations = self.get_relations()

        search_by = DataUtils.filter_search_fields(search_by, self.model)

        if not with_soft_deleted and ('id' in search_by and search_by['id'] is not None):
            uncached_ids = []
            ids = search_by['id'] if isinstance(search_by['id'], list) else [search_by['id']]

            for id in ids:
                prefix = 'user_with_relations' if with_relations else 'user'
                key = redis_client.create_key(prefix, id)
                cached_user = await redis_client.get(key)

                if cached_user:
                    stringified_users_list.append(cached_user)
                else:
                    uncached_ids.append(id)

            if uncached_ids:
                search_by = {"id": uncached_ids}

                result = (
                    await self.get_all_with_joinedload(relations, with_soft_deleted, search_by) 
                    if with_relations else 
                    await self.get_all(search_by, with_soft_deleted)
                )

                if result:
                    for user in result:
                        user_dict = self.model.nested_models_to_dict(user)
                        clean_dict = json.loads(json.dumps(user_dict, default=str))
                        stringified_user = json.dumps(user_dict, default=str)
                        stringified_users_list.append(stringified_user)
                        prefix = 'user_with_relations' if with_relations else 'user'
                        key = redis_client.create_key(prefix, user.id)
                        tags = CacheUtils.extract_cache_tags_from_dto(UserDTO(**clean_dict))

                        data = RedisSetexWithTagsRequestDTO(
                            name=key,
                            time=getenv('USER_TTL'),
                            value=stringified_user,
                            tags=tags,
                        )

                        await redis_client.setex_with_tags(**data.model_dump())

            if not stringified_users_list:
                return []
            
            return [UserDTO(**json.loads(user)) for user in stringified_users_list]

        elif not search_by and not with_soft_deleted:
            key = redis_client.create_key('users_with_relations' if with_relations else 'users')
            stringified_users_list = await redis_client.get(key)

            if not stringified_users_list:
                result = (
                    await self.get_all_with_joinedload(relations, with_soft_deleted) 
                    if with_relations else 
                    await self.get_all(with_soft_deleted)
                )
            
                if not result:
                    return []
                
                stringified_users_list = json.dumps(
                    User.nested_models_to_dict(result), 
                    default=str
                )

                data = RedisSetexRequestDTO(
                    name=key, 
                    time=getenv('USER_TTL'),
                    value=stringified_users_list
                )

                await redis_client.setex(**data.model_dump())

            return [UserDTO(**user_with_relations) for user_with_relations 
                    in json.loads(stringified_users_list)]
        
        else:
            result = (
                await self.get_all_with_joinedload(relations, with_soft_deleted, search_by) 
                if with_relations else 
                await self.get_all(search_by, with_soft_deleted)
            )
            
            if not result:
                return []
                
            return [UserDTO(**User.nested_models_to_dict(user)) for user in result]