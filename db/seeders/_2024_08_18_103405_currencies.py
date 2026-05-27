import asyncio
from models import Currency
from db.seeders.base.base_seeder import BaseSeeder

class Currencies(BaseSeeder):
    revision: str = '_2024_08_18_103405'

    def __init__(self):
        super().__init__(Currency)

        async def seed():
            data_list = [
                Currency(currency='KZT'),
                Currency(currency='RUB'),
                Currency(currency='USD'),
                Currency(currency='EUR')
            ]

            await self.seed(data_list)
            
        asyncio.run(seed())