from errors.base.base_custom_error import BaseCustomError
from utils import DataUtils


class BankAccountNotFoundError(BaseCustomError):
    def __init__(self):
        super().__init__(DataUtils.responses.bank_account_not_found_error)
