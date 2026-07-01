from exceptions.base.base_custom_exception import BaseCustomException
from utils import DataUtils


class PurchaseNotFoundException(BaseCustomException):
    def __init__(self):
        super().__init__(DataUtils.responses.purchase_not_found_error)
