from utils import DataUtils
from exceptions.base.base_custom_exception import BaseCustomException

class UserNotFoundException(BaseCustomException):
    def __init__(self):
        super().__init__(DataUtils.responses.user_not_found_error)