from database.base.database import Database

class BaseSeeder:
    async def seed(self, data_list):
        database = Database()
        await database.init_tables()
        await database.seed(data_list)
        await database.dispose_engine()

    @classmethod
    def get_related(cls, instances, **conditions):
        def matches(instance):
            return all(getattr(instance, key) == value for key, value in conditions.items())
        
        return next(instance for instance in instances if matches(instance))