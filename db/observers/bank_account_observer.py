from sqlalchemy import select

from db.observers.base.base_observer import BaseObserver
from models import BankAccount, Purchase
from repositories.base.redis_client import RedisClient


class BankAccountObserver(BaseObserver):
    model = BankAccount

    @classmethod
    def _get_redis_keys_for_cleanup(cls, event_type: str, target, connection) -> list:
        keys = []
        redis_client = RedisClient()

        keys.append(redis_client.create_key('bank_accounts'))
        keys.append(redis_client.create_key('bank_accounts_with_relations'))
        keys.append(redis_client.create_key('users'))
        keys.append(redis_client.create_key('users_with_relations'))
        keys.append(redis_client.create_key('user', target.user_id))
        keys.append(redis_client.create_key('user_with_relations', target.user_id))
        keys.append(redis_client.create_key('user_bank_accounts', target.user_id))
        keys.append(redis_client.create_key('user_bank_accounts_with_relations', target.user_id))

        if event_type in ('update', 'delete'):
            keys.append(redis_client.create_key('bank_account', target.id))
            keys.append(redis_client.create_key('bank_account_with_relations', target.id))

            query = select(Purchase.id).where(Purchase.account_id == target.id)
            purchase_ids = connection.execute(query).scalars().all()

            for purchase_id in purchase_ids:
                keys.append(redis_client.create_key('purchase', purchase_id))

            if purchase_ids:
                keys.append(redis_client.create_key('purchases'))

        return keys
