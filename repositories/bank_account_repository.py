import json
from os import getenv

from dto import BankAccountDTO, RedisSetexRequestDTO, RedisSetexWithTagsRequestDTO
from models import BankAccount
from repositories.base.base_repository import BaseRepository
from repositories.base.redis_client import RedisClient
from utils import CacheUtils, DataUtils


class BankAccountRepository(BaseRepository):
    model = BankAccount

    async def create_bank_account(self, bank_account_dto: BankAccountDTO) -> None:
        bank_account = self.model(**bank_account_dto.model_dump())
        await self.create(bank_account)

    async def get_bank_account(
        self, search_by: dict, with_relations: bool = False, with_soft_deleted: bool = False
    ) -> BankAccountDTO | None:
        relations = []
        redis_client = RedisClient()

        if with_relations:
            relations = self.get_relations()

        search_by = DataUtils.filter_search_fields(search_by, self.model)

        prefix = "bank_account_with_relations" if with_relations else "bank_account"
        key = redis_client.create_key(prefix, DataUtils.dict_to_model(search_by).id)
        stringified_bank_account = None if with_soft_deleted else await redis_client.get(key)

        if not stringified_bank_account:
            result = (
                await self.get_one_or_none_with_joinedload(search_by, relations, with_soft_deleted)
                if with_relations
                else await self.get_one_or_none(search_by, with_soft_deleted)
            )

            if not result:
                return None

            bank_account_dict = self.model.nested_models_to_dict(result)
            clean_dict = json.loads(json.dumps(bank_account_dict, default=str))
            stringified_bank_account = json.dumps(bank_account_dict, default=str)
            tags = CacheUtils.extract_cache_tags_from_dto(BankAccountDTO(**clean_dict))

            data = RedisSetexWithTagsRequestDTO(
                name=key,
                time=getenv("FIN_DATA_TTL"),
                value=stringified_bank_account,
                tags=tags,
            )

            if not with_soft_deleted:
                await redis_client.setex_with_tags(**data.model_dump())

        return BankAccountDTO(**json.loads(stringified_bank_account))

    async def get_bank_accounts(
        self, search_by: dict, with_relations: bool, with_soft_deleted: bool = False
    ) -> list[BankAccountDTO]:
        relations = []
        stringified_bank_accounts_list = []
        redis_client = RedisClient()

        if with_relations:
            relations = self.get_relations()

        search_by = DataUtils.filter_search_fields(search_by, self.model)

        if not with_soft_deleted and (
            ("id" in search_by and search_by["id"] is not None)
            or ("user_id" in search_by and search_by["user_id"] is not None)
        ):
            user_id = search_by.get("user_id")

            if "id" in search_by and search_by["id"] is not None:
                uncached_ids = []
                ids = search_by["id"] if isinstance(search_by["id"], list) else [search_by["id"]]

                for id in ids:
                    prefix = "bank_account_with_relations" if with_relations else "bank_account"
                    key = redis_client.create_key(prefix, id)
                    cached_bank_account = await redis_client.get(key)

                    if cached_bank_account:
                        stringified_bank_accounts_list.append(cached_bank_account)
                    else:
                        uncached_ids.append(id)

                if uncached_ids:
                    search_by = {"id": uncached_ids}
                    if user_id is not None:
                        search_by["user_id"] = user_id

                    result = (
                        await self.get_all_with_joinedload(relations, with_soft_deleted, search_by)
                        if with_relations
                        else await self.get_all(search_by, with_soft_deleted)
                    )

                    if result:
                        for bank_account in result:
                            bank_account_dict = self.model.nested_models_to_dict(bank_account)
                            clean_dict = json.loads(json.dumps(bank_account_dict, default=str))
                            stringified_bank_account = json.dumps(bank_account_dict, default=str)
                            stringified_bank_accounts_list.append(stringified_bank_account)
                            prefix = "bank_account_with_relations" if with_relations else "bank_account"
                            key = redis_client.create_key(prefix, bank_account.id)
                            tags = CacheUtils.extract_cache_tags_from_dto(BankAccountDTO(**clean_dict))

                            data = RedisSetexWithTagsRequestDTO(
                                name=key,
                                time=getenv("FIN_DATA_TTL"),
                                value=stringified_bank_account,
                                tags=tags,
                            )

                            await redis_client.setex_with_tags(**data.model_dump())

                if not stringified_bank_accounts_list:
                    return []

                dto_list = [
                    BankAccountDTO(**json.loads(bank_account)) for bank_account in stringified_bank_accounts_list
                ]

                if user_id is not None:
                    dto_list = [dto for dto in dto_list if dto.user_id == user_id]

                return dto_list

            prefix = "user_bank_accounts_with_relations" if with_relations else "user_bank_accounts"
            key = redis_client.create_key(prefix, user_id)
            stringified_user_bank_accounts_list = await redis_client.get(key)

            if not stringified_user_bank_accounts_list:
                result = (
                    await self.get_all_with_joinedload(relations, with_soft_deleted, {"user_id": user_id})
                    if with_relations
                    else await self.get_all({"user_id": user_id}, with_soft_deleted)
                )

                if not result:
                    return []

                stringified_user_bank_accounts_list = json.dumps(BankAccount.nested_models_to_dict(result), default=str)

                data = RedisSetexRequestDTO(
                    name=key, time=getenv("FIN_DATA_TTL"), value=stringified_user_bank_accounts_list
                )

                await redis_client.setex(**data.model_dump())

            return [BankAccountDTO(**item) for item in json.loads(stringified_user_bank_accounts_list)]

        if not search_by and not with_soft_deleted:
            key = redis_client.create_key("bank_accounts_with_relations" if with_relations else "bank_accounts")
            stringified_bank_accounts_list = await redis_client.get(key)

            if not stringified_bank_accounts_list:
                result = (
                    await self.get_all_with_joinedload(relations, with_soft_deleted)
                    if with_relations
                    else await self.get_all(with_soft_deleted)
                )

                if not result:
                    return []

                stringified_bank_accounts_list = json.dumps(BankAccount.nested_models_to_dict(result), default=str)

                data = RedisSetexRequestDTO(name=key, time=getenv("FIN_DATA_TTL"), value=stringified_bank_accounts_list)

                await redis_client.setex(**data.model_dump())

            return [
                BankAccountDTO(**bank_account_with_relations)
                for bank_account_with_relations in json.loads(stringified_bank_accounts_list)
            ]

        result = (
            await self.get_all_with_joinedload(relations, with_soft_deleted, search_by)
            if with_relations
            else await self.get_all(search_by, with_soft_deleted)
        )

        if not result:
            return []

        return [BankAccountDTO(**BankAccount.nested_models_to_dict(bank_account)) for bank_account in result]

    async def delete_bank_account(self, search_by: dict, soft_delete: bool) -> None:
        search_by = DataUtils.filter_search_fields(search_by, self.model)
        await self.delete(soft_delete, search_by)

    async def delete_all_bank_accounts(self, soft_delete: bool) -> None:
        await self.bulk_delete(soft_delete)
        await CacheUtils.cascade_invalidate_bank_account_cache(RedisClient())
