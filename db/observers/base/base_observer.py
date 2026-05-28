from sqlalchemy import event

class BaseObserver:
    model = None

    @classmethod
    def register(cls):
        if cls.model is None:
            raise ValueError(f"Observer '{cls.__name__}' must define a 'model' attribute")

        possible_events = [
            'before_insert', 
            'after_insert',
            'before_update', 
            'after_update',
            'before_delete', 
            'after_delete'
        ]

        for event_name in possible_events:
            if hasattr(cls, event_name):
                method = getattr(cls, event_name)
                event.listen(cls.model, event_name, method)