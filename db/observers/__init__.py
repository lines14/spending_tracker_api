from .bank_account_observer import BankAccountObserver

_observers = [
    BankAccountObserver
]

def init_observers():
    for observer in _observers:
        observer.register()