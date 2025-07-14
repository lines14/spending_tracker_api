import json
from typing import Optional
from models import BankAccount
from DTO import BankAccountDTO, RedisSetRequestDTO
from repositories.base.redis_client import RedisClient

class BankAccountRepository:    
    async def create_bank_account(self, bank_account: BankAccountDTO) -> None:
        redis_client = RedisClient()

        new_bank_account = BankAccount(**bank_account.model_dump())
        await new_bank_account.create()

        name = redis_client.create_key('bank_account', new_bank_account.id)
        new_stringified_bank_account = json.dumps(new_bank_account.to_dict(), default=str)

        data = RedisSetRequestDTO(
            name=name, 
            value=new_stringified_bank_account
        )

        await redis_client.set(**data.model_dump())

    async def get_bank_account(self, id: int) -> Optional[BankAccountDTO]:
        redis_client = RedisClient()
        name = redis_client.create_key('bank_account', id)
        stringified_bank_account = await redis_client.get(name)

        if not stringified_bank_account:
            result = await BankAccount(id=id).get()

            if not result:
                return None

            bank_account = result.pop()
            stringified_bank_account = json.dumps(bank_account.to_dict(), default=str)

            data = RedisSetRequestDTO(
                name=name, 
                value=stringified_bank_account
            )

            await redis_client.set(**data.model_dump())

        return BankAccountDTO(**json.loads(stringified_bank_account))
    
    async def get_bank_accounts(self) -> list[BankAccountDTO]:
        redis_client = RedisClient()
        name = redis_client.create_key('bank_accounts')
        stringified_bank_accounts = await redis_client.get(name)

        if not stringified_bank_accounts:
            result = await BankAccount().get()
        
            stringified_bank_accounts = json.dumps(BankAccount.nested_models_to_dict(result), default=str)

            data = RedisSetRequestDTO(
                name=name, 
                value=stringified_bank_accounts
            )

            await redis_client.set(**data.model_dump())

        return [BankAccountDTO(**item) for item in json.loads(stringified_bank_accounts)]

    async def delete_bank_account(self, id: int, soft_delete: bool) -> None:
        redis_client = RedisClient()
        name = redis_client.create_key('bank_account', id)
        await redis_client.delete(name)
        
        await BankAccount(id=id).delete(soft_delete)

    async def delete_bank_accounts(self, soft_delete: bool) -> None:
        redis_client = RedisClient()
        name = redis_client.create_key('bank_accounts')
        await redis_client.delete(name)
        
        await BankAccount().delete(soft_delete)