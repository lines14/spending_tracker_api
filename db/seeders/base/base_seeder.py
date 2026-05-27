from db.db import DB

class BaseSeeder:
    async def seed(self, data_list):
        db = DB()
        await db.init_tables()
        await db.seed(data_list)
        await db.dispose_engine()

    @classmethod
    def get_related(cls, instances, **conditions):
        def matches(instance):
            return all(getattr(instance, key) == value for key, value in conditions.items())
        
        return next(instance for instance in instances if matches(instance))