from sqlalchemy import event, inspect

from repositories.base.redis_client import RedisClient


class BaseObserver:
    model = None

    @classmethod
    def register(cls):
        if cls.model is None:
            raise ValueError(f"Observer '{cls.__name__}' must define a 'model' attribute")

        possible_events = [
            "before_insert",
            "after_insert",
            "before_update",
            "after_update",
            "before_delete",
            "after_delete",
        ]

        for event_name in possible_events:
            if hasattr(cls, event_name):
                method = getattr(cls, event_name)
                event.listen(cls.model, event_name, method)

    @classmethod
    def _get_redis_keys_for_cleanup(cls, event_type: str, target, connection) -> list:
        raise NotImplementedError

    @classmethod
    def __clear_cache(cls, event_type: str, target, connection):
        keys = cls._get_redis_keys_for_cleanup(event_type, target, connection)

        if not keys:
            return

        session = inspect(target).session

        if session:

            @event.listens_for(session, "after_commit", once=True)
            def _on_commit():
                redis_client = RedisClient()

                for key in keys:
                    redis_client.sync_delete(key)

                print(
                    f"INFO:     [Observer] Cache invalidated for '{cls.model.__name__}:{target.id}' and relations on {event_type.upper()} event"
                )

    @classmethod
    def after_insert(cls, _mapper, connection, target):
        cls.__clear_cache("insert", target, connection)

    @classmethod
    def after_update(cls, _mapper, connection, target):
        cls.__clear_cache("update", target, connection)

    @classmethod
    def after_delete(cls, _mapper, connection, target):
        cls.__clear_cache("delete", target, connection)
