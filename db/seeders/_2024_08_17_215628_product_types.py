import asyncio
from models import ProductType, ProductGroup
from db.seeders.base.base_seeder import BaseSeeder
from repositories.base.base_repository import BaseRepository

class ProductTypes(BaseSeeder):
    revision: str = '_2024_08_17_215628'

    def __init__(self):
        super().__init__(ProductType)

        async def seed():
            product_group_repository = BaseRepository(ProductGroup)
            product_groups = await product_group_repository.get_all()

            data_list = [
                ProductType(
                    group_id=self.get_related(product_groups, group='Продукты').id, 
                    type='Овощи'
                ),
                ProductType(
                    group_id=self.get_related(product_groups, group='Продукты').id, 
                    type='Фрукты и ягоды'
                ),
                ProductType(
                    group_id=self.get_related(product_groups, group='Продукты').id, 
                    type='Молочные продукты'
                ),
                ProductType(
                    group_id=self.get_related(product_groups, group='Продукты').id, 
                    type='Мясные продукты'
                ),
                ProductType(
                    group_id=self.get_related(product_groups, group='Продукты').id, 
                    type='Замороженные продукты'
                ),
                ProductType(
                    group_id=self.get_related(product_groups, group='Продукты').id, 
                    type='Бакалея'
                ),
                ProductType(
                    group_id=self.get_related(product_groups, group='Продукты').id, 
                    type='Алкогольные напитки'
                ),
                ProductType(
                    group_id=self.get_related(product_groups, group='Бытовые товары').id, 
                    type='Личная гигиена'
                ),
                ProductType(
                    group_id=self.get_related(product_groups, group='Бытовые товары').id, 
                    type='Уборка'
                )
            ]

            await self.seed(data_list)
            
        asyncio.run(seed())