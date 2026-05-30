from models import Purchase
from repositories.base.redis_client import RedisClient
from db.observers.base.base_observer import BaseObserver

class PurchaseObserver(BaseObserver):
    model = Purchase

    @classmethod
    def _get_redis_keys_for_cleanup(cls, event_type: str, target) -> list:
        keys = []
        redis_client = RedisClient()

        keys.append(redis_client.create_key('purchases'))
        keys.append(redis_client.create_key('bank_accounts'))
        keys.append(redis_client.create_key('bank_account', target.account_id))
        keys.append(redis_client.create_key('bank_account_with_relations', target.account_id))
        keys.append(redis_client.create_key('user', target.user_id))
        keys.append(redis_client.create_key('user_with_relations', target.user_id))

        if event_type in ('update', 'delete'):
            keys.append(redis_client.create_key('purchase', target.id))

        return keys