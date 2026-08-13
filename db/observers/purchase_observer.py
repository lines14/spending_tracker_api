from sqlalchemy import select

from db.observers.base.base_observer import BaseObserver
from models import BankAccount, Purchase
from repositories.base.redis_client import RedisClient


class PurchaseObserver(BaseObserver):
    model = Purchase

    @classmethod
    def _get_redis_keys_for_cleanup(cls, event_type: str, target, connection) -> list:
        keys = []
        redis_client = RedisClient.get_instance()

        keys.append(redis_client.create_key("purchases"))
        keys.append(redis_client.create_key("bank_accounts"))
        keys.append(redis_client.create_key("bank_accounts_with_relations"))
        keys.append(redis_client.create_key("users"))
        keys.append(redis_client.create_key("users_with_relations"))
        keys.append(redis_client.create_key("bank_account", target.account_id))
        keys.append(redis_client.create_key("bank_account_with_relations", target.account_id))

        query = select(BankAccount.user_id).where(BankAccount.id == target.account_id)
        user_id = connection.execute(query).scalar()

        keys.append(redis_client.create_key("user", user_id))
        keys.append(redis_client.create_key("user_with_relations", user_id))
        keys.append(redis_client.create_key("user_bank_accounts", user_id))
        keys.append(redis_client.create_key("user_bank_accounts_with_relations", user_id))

        if event_type in ("update", "delete"):
            keys.append(redis_client.create_key("purchase", target.id))

        return keys
