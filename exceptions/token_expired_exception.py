from utils import DataUtils
from exceptions.base.base_custom_exception import BaseCustomException

class TokenExpiredException(BaseCustomException):
    def __init__(self):
        super().__init__(DataUtils.responses.token_expired_error)