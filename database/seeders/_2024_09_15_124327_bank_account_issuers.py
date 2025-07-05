import asyncio
from models import BankAccountIssuer
from database.base.database import Database
from database.seeders.base.base_seeder import BaseSeeder

class BankAccountIssuers(BaseSeeder):
    revision: str = '_2024_09_15_124327'

    def __init__(self):
        async def seed():
            await Database().seed([
                BankAccountIssuer(issuer='Kaspi', country_code='KAZ'),
                BankAccountIssuer(issuer='Halyk', country_code='KAZ'),
                BankAccountIssuer(issuer='Freedom', country_code='KAZ'),
                BankAccountIssuer(issuer='Homecredit', country_code='KAZ'),
                BankAccountIssuer(issuer='BCC', country_code='KAZ'),
                BankAccountIssuer(issuer='Jusan', country_code='KAZ'),
                BankAccountIssuer(issuer='Forte', country_code='KAZ'),
                BankAccountIssuer(issuer='Bereke', country_code='KAZ'),
                BankAccountIssuer(issuer='Sberbank', country_code='RUS'),
                BankAccountIssuer(issuer='VTB', country_code='RUS'),
                BankAccountIssuer(issuer='OTP', country_code='RUS')
            ])
            
        asyncio.run(seed())
