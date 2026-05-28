from models import BankAccount
from repositories.base.redis_client import RedisClient
from db.observers.base.base_observer import BaseObserver

class BankAccountObserver(BaseObserver):
    model = BankAccount

    @classmethod
    def __clear_cache(cls, target):
        redis_client = RedisClient()

        key = redis_client.create_key('bank_account', target.id)
        list_key = redis_client.create_key('bank_accounts')
        parent_key = redis_client.create_key('user', target.user_id)
        parent_with_relations_key = redis_client.create_key('user_with_relations', target.user_id)

        redis_client.sync_delete(key)
        redis_client.sync_delete(list_key)
        redis_client.sync_delete(parent_key)
        redis_client.sync_delete(parent_with_relations_key)

        print(f"INFO:     [Observer] Cache invalidated for '{cls.model.__name__}:{target.id}' and relations")

    @classmethod
    def after_update(cls, mapper, connection, target):
        cls.__clear_cache(target)

    @classmethod
    def after_delete(cls, mapper, connection, target):
        cls.__clear_cache(target)
    
    @classmethod
    def after_insert(cls, mapper, connection, target):
        redis_client = RedisClient()

        list_key = redis_client.create_key('bank_accounts')
        parent_key = redis_client.create_key('user', target.user_id)
        parent_with_relations_key = redis_client.create_key('user_with_relations', target.user_id)

        redis_client.sync_delete(list_key)
        redis_client.sync_delete(parent_key)
        redis_client.sync_delete(parent_with_relations_key)
        
        print(f"INFO:     [Observer] Cache invalidated for relations of new '{cls.model.__name__}:{target.id}'")