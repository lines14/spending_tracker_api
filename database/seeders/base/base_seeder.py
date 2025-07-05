class BaseSeeder:
    @classmethod
    def get_related(cls, instances, **conditions):
        def matches(instance):
            return all(getattr(instance, key) == value for key, value in conditions.items())
        
        return next(instance for instance in instances if matches(instance))