from models import Purchase
from repositories.base.redis_client import RedisClient
from db.observers.base.base_observer import BaseObserver

class PurchaseObserver(BaseObserver):
    model = Purchase

    @classmethod
    def __clear_cache(cls, target):
        keys = []
        redis_client = RedisClient()

        keys.append(redis_client.create_key('purchase', target.id))
        keys.append(redis_client.create_key('purchases'))
        keys.append(redis_client.create_key('bank_accounts'))
        keys.append(redis_client.create_key('bank_account', target.account_id))
        keys.append(redis_client.create_key('bank_account_with_relations', target.account_id))
        keys.append(redis_client.create_key('user', target.user_id))
        keys.append(redis_client.create_key('user_with_relations', target.user_id))

        for key in keys:
            redis_client.sync_delete(key)

        print(f"INFO:     [Observer] Cache invalidated for '{cls.model.__name__}:{target.id}' and relations")

    @classmethod
    def after_update(cls, mapper, connection, target):
        cls.__clear_cache(target)

    @classmethod
    def after_delete(cls, mapper, connection, target):
        cls.__clear_cache(target)
    
    @classmethod
    def after_insert(cls, mapper, connection, target):
        keys = []
        redis_client = RedisClient()

        keys.append(redis_client.create_key('purchases'))
        keys.append(redis_client.create_key('bank_accounts'))
        keys.append(redis_client.create_key('bank_account', target.account_id))
        keys.append(redis_client.create_key('bank_account_with_relations', target.account_id))
        keys.append(redis_client.create_key('user', target.user_id))
        keys.append(redis_client.create_key('user_with_relations', target.user_id))

        for key in keys:
            redis_client.sync_delete(key)
        
        print(f"INFO:     [Observer] Cache invalidated for '{cls.model.__name__}:{target.id}' and relations")