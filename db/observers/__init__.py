from .user_observer import UserObserver
from .purchase_observer import PurchaseObserver
from .bank_account_observer import BankAccountObserver

_observers = [
    UserObserver,
    PurchaseObserver,
    BankAccountObserver
]

def init_observers():
    for observer in _observers:
        observer.register()