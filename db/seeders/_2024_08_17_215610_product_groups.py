import asyncio
from models import ProductGroup
from db.seeders.base.base_seeder import BaseSeeder

class ProductGroups(BaseSeeder):
    revision: str = '_2024_08_17_215610'

    def __init__(self):
        super().__init__(ProductGroup)
        
        async def seed():
            data_list = [
                ProductGroup(group='Продукты'),
                ProductGroup(group='Бытовые товары'),
                ProductGroup(group='Электроника'),
                ProductGroup(group='Одежда'),
                ProductGroup(group='Услуги')
            ]

            await self.seed(data_list)
            
        asyncio.run(seed())