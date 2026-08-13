from sqlalchemy import select, inspect

from db.observers.base.base_observer import BaseObserver
from models import BankAccount, Purchase, User
from repositories.base.redis_client import RedisClient


class UserObserver(BaseObserver):
    model = User

    @classmethod
    def _get_redis_keys_for_cleanup(cls, event_type: str, target, connection) -> list:
        keys = []
        redis_client = RedisClient()

        keys.append(redis_client.create_key("users"))
        keys.append(redis_client.create_key("users_with_relations"))
        keys.append(redis_client.create_key("bank_accounts"))
        keys.append(redis_client.create_key("bank_accounts_with_relations"))
        keys.append(redis_client.create_key("purchases"))

        if event_type in ("update", "delete"):
            keys.append(redis_client.create_key("user", target.id))
            keys.append(redis_client.create_key("user_with_relations", target.id))
            keys.append(redis_client.create_key(target.login))

            if event_type == "delete" or cls._login_or_password_is_changed(target):
                keys.append(redis_client.create_key("session", target.id))                

            query = select(BankAccount.id).where(BankAccount.user_id == target.id)
            bank_account_ids = connection.execute(query).scalars().all()

            for bank_account_id in bank_account_ids:
                keys.append(redis_client.create_key("bank_account", bank_account_id))
                keys.append(redis_client.create_key("bank_account_with_relations", bank_account_id))

                query = select(Purchase.id).where(Purchase.account_id == bank_account_id)
                purchase_ids = connection.execute(query).scalars().all()
                for purchase_id in purchase_ids:
                    keys.append(redis_client.create_key("purchase", purchase_id))

            keys.append(redis_client.create_key("user_bank_accounts", target.id))
            keys.append(redis_client.create_key("user_bank_accounts_with_relations", target.id))

        return keys

    @classmethod
    def _login_or_password_is_changed(cls, target) -> bool:
        login_changed = False
        password_changed = False
        state = inspect(target)

        if "login" in state.attrs and hasattr(state.attrs.login, "history"):
            login_changed = state.attrs.login.history.has_changes()

        if "hashed_password" in state.attrs and hasattr(state.attrs.hashed_password, "history"):
            password_changed = state.attrs.hashed_password.history.has_changes()

        # return login_changed or password_changed
        return password_changed