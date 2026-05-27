import asyncio
from models import ProductType, ProductSubType
from db.seeders.base.base_seeder import BaseSeeder

class ProductSubTypes(BaseSeeder):
    revision: str = '_2024_08_18_093345'

    def __init__(self):
        async def seed():
            product_types = await ProductType().get()

            data_list = [
                ProductSubType(
                    type_id=self.get_related(product_types, type='Овощи').id, 
                    sub_type='Огурцы'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Овощи').id, 
                    sub_type='Помидоры'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Овощи').id, 
                    sub_type='Помидоры черри'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Овощи').id, 
                    sub_type='Салат'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Овощи').id, 
                    sub_type='Баклажан'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Овощи').id, 
                    sub_type='Кабачок'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Овощи').id, 
                    sub_type='Лук репчатый'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Овощи').id, 
                    sub_type='Лук красный'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Овощи').id, 
                    sub_type='Лук зелёный'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Овощи').id, 
                    sub_type='Перец чили'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Овощи').id, 
                    sub_type='Перец сладкий'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Овощи').id, 
                    sub_type='Картофель'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Овощи').id, 
                    sub_type='Капуста белокочанная'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Овощи').id, 
                    sub_type='Капуста брюссельская'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Овощи').id, 
                    sub_type='Капуста брокколи'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Овощи').id, 
                    sub_type='Капуста цветная'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Фрукты и ягоды').id, 
                    sub_type='Мандарины'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Фрукты и ягоды').id, 
                    sub_type='Апельсины'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Фрукты и ягоды').id, 
                    sub_type='Бананы'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Фрукты и ягоды').id, 
                    sub_type='Грейпфрут'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Фрукты и ягоды').id, 
                    sub_type='Арбуз'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Фрукты и ягоды').id, 
                    sub_type='Дыня'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Фрукты и ягоды').id, 
                    sub_type='Клубника'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Фрукты и ягоды').id, 
                    sub_type='Лимон'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Фрукты и ягоды').id, 
                    sub_type='Сливы'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Фрукты и ягоды').id, 
                    sub_type='Киви'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Фрукты и ягоды').id, 
                    sub_type='Виноград'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Фрукты и ягоды').id, 
                    sub_type='Яблоки'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Фрукты и ягоды').id, 
                    sub_type='Нектарины'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Фрукты и ягоды').id, 
                    sub_type='Персики'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Фрукты и ягоды').id, 
                    sub_type='Груши'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Молочные продукты').id, 
                    sub_type='Сыр'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Молочные продукты').id, 
                    sub_type='Сырки'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Молочные продукты').id, 
                    sub_type='Творог'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Молочные продукты').id, 
                    sub_type='Творожная масса'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Молочные продукты').id, 
                    sub_type='Творожный десерт'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Молочные продукты').id, 
                    sub_type='Йогурт ложковый'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Молочные продукты').id, 
                    sub_type='Йогурт питьевой'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Молочные продукты').id, 
                    sub_type='Молоко'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Молочные продукты').id, 
                    sub_type='Топлёное молоко'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Молочные продукты').id, 
                    sub_type='Кефир'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Молочные продукты').id, 
                    sub_type='Ряженка'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Молочные продукты').id, 
                    sub_type='Варенец'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Мясные продукты').id, 
                    sub_type='Фарш'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Мясные продукты').id, 
                    sub_type='Ветчина'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Мясные продукты').id, 
                    sub_type='Карбонад'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Мясные продукты').id, 
                    sub_type='Колбаса'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Мясные продукты').id, 
                    sub_type='Готовое мясо'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Мясные продукты').id, 
                    sub_type='Сырое мясо'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Мясные продукты').id, 
                    sub_type='Сосиски'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Мясные продукты').id, 
                    sub_type='Сардельки'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Мясные продукты').id, 
                    sub_type='Шпикачки'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Замороженные продукты').id, 
                    sub_type='Пельмени'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Замороженные продукты').id, 
                    sub_type='Вареники'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Замороженные продукты').id, 
                    sub_type='Хинкали'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Замороженные продукты').id, 
                    sub_type='Наггетсы'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Замороженные продукты').id, 
                    sub_type='Котлеты'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Замороженные продукты').id, 
                    sub_type='Голубцы'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Замороженные продукты').id, 
                    sub_type='Фаршированные перцы'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Замороженные продукты').id, 
                    sub_type='Долма'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Замороженные продукты').id, 
                    sub_type='Овощная смесь'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Замороженные продукты').id, 
                    sub_type='Замороженные ягоды'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Замороженные продукты').id, 
                    sub_type='Фруктовая смесь'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Замороженные продукты').id, 
                    sub_type='Драники'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Замороженные продукты').id, 
                    sub_type='Сырники'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Замороженные продукты').id, 
                    sub_type='Чебуреки'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Замороженные продукты').id, 
                    sub_type='Пицца'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Бакалея').id, 
                    sub_type='Хлеб'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Бакалея').id, 
                    sub_type='Сок'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Бакалея').id, 
                    sub_type='Квас'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Бакалея').id, 
                    sub_type='Специи'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Бакалея').id, 
                    sub_type='Минеральная вода'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Бакалея').id, 
                    sub_type='Газированная вода'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Бакалея').id, 
                    sub_type='Томатная паста'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Бакалея').id, 
                    sub_type='Рис'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Бакалея').id, 
                    sub_type='Макароны'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Бакалея').id, 
                    sub_type='Гречка'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Бакалея').id, 
                    sub_type='Булгур'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Бакалея').id, 
                    sub_type='Сахар'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Бакалея').id, 
                    sub_type='Фруктоза'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Бакалея').id, 
                    sub_type='Соль'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Бакалея').id, 
                    sub_type='Соус'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Бакалея').id, 
                    sub_type='Кетчуп'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Бакалея').id, 
                    sub_type='Сладкие батончики'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Бакалея').id, 
                    sub_type='Конфеты'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Алкогольные напитки').id, 
                    sub_type='Пиво'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Алкогольные напитки').id, 
                    sub_type='Водка'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Алкогольные напитки').id, 
                    sub_type='Виски'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Алкогольные напитки').id, 
                    sub_type='Вино'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Личная гигиена').id, 
                    sub_type='Мыло'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Личная гигиена').id, 
                    sub_type='Шампунь'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Личная гигиена').id, 
                    sub_type='Зубная паста'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Личная гигиена').id, 
                    sub_type='Зубная щётка'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Личная гигиена').id, 
                    sub_type='Бритвенные станки'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Личная гигиена').id, 
                    sub_type='Средство для бритья'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Личная гигиена').id, 
                    sub_type='Туалетная бумага'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Личная гигиена').id, 
                    sub_type='Влажные салфетки'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Личная гигиена').id, 
                    sub_type='Салфетки'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Уборка').id, 
                    sub_type='Губки'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Уборка').id, 
                    sub_type='Перчатки'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Уборка').id, 
                    sub_type='Тряпки'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Уборка').id, 
                    sub_type='Освежитель воздуха'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Уборка').id, 
                    sub_type='Ролик для одежды'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Уборка').id, 
                    sub_type='Чистящий порошок'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Уборка').id, 
                    sub_type='Стиральный порошок'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Уборка').id, 
                    sub_type='Средство для мытья полов'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Уборка').id, 
                    sub_type='Средство для мытья туалета'
                ),
                ProductSubType(
                    type_id=self.get_related(product_types, type='Уборка').id, 
                    sub_type='Средство для мытья посуды'
                )
            ]

            await self.seed(data_list)
            
        asyncio.run(seed())