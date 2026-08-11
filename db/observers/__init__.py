from .bank_account_observer import BankAccountObserver
from .purchase_observer import PurchaseObserver
from .user_observer import UserObserver

_observers = [UserObserver, PurchaseObserver, BankAccountObserver]


def init_observers():
    for observer in _observers:
        observer.register()
