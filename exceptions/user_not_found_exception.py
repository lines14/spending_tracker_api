from exceptions.base.base_custom_exception import BaseCustomException
from utils import DataUtils


class UserNotFoundException(BaseCustomException):
    def __init__(self):
        super().__init__(DataUtils.responses.user_not_found_error)
