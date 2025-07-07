import json
from typing import Optional
from DTO import BankAccountDTO
from models import BankAccount

class BankAccountRepository:    
    async def create_bank_account(self, bank_account: BankAccountDTO) -> None:
        await BankAccount(**vars(bank_account)).create()

    async def get_bank_account(self, id: int) -> Optional[BankAccountDTO]:
        bank_account = await BankAccount(id=id).get()

        if not bank_account:
            return None
        
        stringified_bank_account = json.dumps(bank_account.to_dict(), default=str)

        return BankAccountDTO(**json.loads(stringified_bank_account))

    async def delete_bank_account(self, id: int) -> None:
        await BankAccount(id=id).delete()