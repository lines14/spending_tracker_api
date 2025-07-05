import asyncio
from models import ProductGroup
from database.base.database import Database
from database.seeders.base.base_seeder import BaseSeeder

class ProductGroups(BaseSeeder):
    revision: str = '_2024_08_17_215610'

    def __init__(self):
        async def seed():
            await Database().seed([
                ProductGroup(group='Продукты'),
                ProductGroup(group='Бытовые товары'),
                ProductGroup(group='Электроника'),
                ProductGroup(group='Одежда'),
                ProductGroup(group='Услуги')
            ])
            
        asyncio.run(seed())