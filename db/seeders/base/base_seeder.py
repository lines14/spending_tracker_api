from db.base.base_db import BaseDB
from repositories.base.base_repository import BaseRepository

class BaseSeeder:
    async def seed(self, data_list):
        db = BaseDB()
        await db.init_tables()
        await BaseRepository.seed(data_list)
        await db.dispose_engine()

    @classmethod
    def get_related(cls, instances, **conditions):
        def matches(instance):
            return all(getattr(instance, key) == value for key, value in conditions.items())
        
        return next(instance for instance in instances if matches(instance))