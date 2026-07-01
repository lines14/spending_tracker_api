from exceptions.base.base_custom_exception import BaseCustomException
from utils import DataUtils


class InvalidCredentialsException(BaseCustomException):
    def __init__(self):
        super().__init__(DataUtils.responses.invalid_credentials_error)
