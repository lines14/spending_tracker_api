from utils import DataUtils
from exceptions.base.base_custom_exception import BaseCustomException

class BankAccountNotFoundException(BaseCustomException):
    def __init__(self):
        super().__init__(DataUtils.responses.bank_account_not_found_error)