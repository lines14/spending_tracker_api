import asyncio
from models import Currency
from database.base.database import Database

class Currencies():
    revision: str = '_2024_08_18_103405'

    def __init__(self):
        async def seed():
            await Database().seed([
                Currency(currency='KZT'),
                Currency(currency='RUB'),
                Currency(currency='USD'),
                Currency(currency='EUR')
            ])
        asyncio.run(seed())