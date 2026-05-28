import json
from utils import DataUtils
from typing import Optional
from models import BankAccount
from dto import BankAccountDTO, RedisSetRequestDTO
from repositories.base.redis_client import RedisClient
from repositories.base.base_repository import BaseRepository

class BankAccountRepository(BaseRepository):   
    def __init__(self):
        super().__init__(model=BankAccount)

    async def create_bank_account(self, bank_account_dto: BankAccountDTO) -> None:
        bank_account = self.model(**bank_account_dto.model_dump())
        await self.create(bank_account)

    async def get_bank_account(self, search_by: dict) -> Optional[BankAccountDTO]:
        redis_client = RedisClient()

        search_by = DataUtils.filter_search_fields(search_by, self.model)
        key = redis_client.create_key('bank_account', DataUtils.dict_to_model(search_by).id)
        stringified_bank_account = await redis_client.get(key)

        if not stringified_bank_account:
            result = await self.get_one_or_none(search_by)

            if not result:
                return None

            stringified_bank_account = json.dumps(result.model_dump(), default=str)

            data = RedisSetRequestDTO(
                name=key, 
                value=stringified_bank_account
            )

            await redis_client.set(**data.model_dump())

        return BankAccountDTO(**json.loads(stringified_bank_account))
    
    async def get_all_bank_accounts(self) -> list[BankAccountDTO]:
        redis_client = RedisClient()
        key = redis_client.create_key('bank_accounts')
        stringified_bank_accounts = await redis_client.get(key)

        if not stringified_bank_accounts:
            result = await self.get_all()
        
            stringified_bank_accounts = json.dumps(BankAccount.nested_models_to_dict(result), default=str)

            data = RedisSetRequestDTO(
                name=key, 
                value=stringified_bank_accounts
            )

            await redis_client.set(**data.model_dump())

        return [BankAccountDTO(**item) for item in json.loads(stringified_bank_accounts)]

    async def delete_bank_account(self, search_by: dict, soft_delete: bool) -> None:
        search_by = DataUtils.filter_search_fields(search_by, self.model)
        await self.delete(soft_delete, search_by)

    async def delete_all_bank_accounts(self, soft_delete: bool) -> None:        
        await self.bulk_delete(soft_delete)