import asyncio

from db.seeders.base.base_seeder import BaseSeeder
from models import BankAccountIssuer


class BankAccountIssuers(BaseSeeder):
    revision: str = '_2024_09_15_124327'

    def __init__(self):
        super().__init__(BankAccountIssuer)

        async def seed():
            data_list = [
                BankAccountIssuer(issuer='Kaspi', country_code='KAZ'),
                BankAccountIssuer(issuer='Halyk', country_code='KAZ'),
                BankAccountIssuer(issuer='Freedom', country_code='KAZ'),
                BankAccountIssuer(issuer='Homecredit', country_code='KAZ'),
                BankAccountIssuer(issuer='BCC', country_code='KAZ'),
                BankAccountIssuer(issuer='Alatau City', country_code='KAZ'),
                BankAccountIssuer(issuer='Forte', country_code='KAZ'),
                BankAccountIssuer(issuer='Bereke', country_code='KAZ'),
                BankAccountIssuer(issuer='Sberbank', country_code='RUS'),
                BankAccountIssuer(issuer='VTB', country_code='RUS'),
                BankAccountIssuer(issuer='OTP', country_code='RUS'),
                BankAccountIssuer(issuer='Cifra', country_code='RUS')
            ]

            await self.seed(data_list)

        asyncio.run(seed())
