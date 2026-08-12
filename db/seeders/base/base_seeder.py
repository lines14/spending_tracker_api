from db.base.base_db import BaseDB
from repositories.base.base_repository import BaseRepository


class BaseSeeder:
    def __init__(self, model):
        self.model = model

    def __await__(self):
        return self.run().__await__()

    async def run(self):
        raise NotImplementedError
    
    async def seed(self, data_list):
        async with BaseDB() as db:
            await db.init_tables()
            repository = BaseRepository(self.model, db.session)
            await repository.seed(data_list)

    async def get_related_records(self, related_model: type) -> list:
        async with BaseDB() as db:
            repository = BaseRepository(related_model, db.session)
            return await repository.get_all()

    @classmethod
    def get_related(cls, instances, **conditions):
        def matches(instance):
            return all(getattr(instance, key) == value for key, value in conditions.items())

        return next(instance for instance in instances if matches(instance))
