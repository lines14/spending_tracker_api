from .purchase_observer import PurchaseObserver
from .bank_account_observer import BankAccountObserver

_observers = [
    PurchaseObserver,
    BankAccountObserver
]

def init_observers():
    for observer in _observers:
        observer.register()