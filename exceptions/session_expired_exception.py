from utils import DataUtils
from exceptions.base.base_custom_exception import BaseCustomException

class SessionExpiredException(BaseCustomException):
    def __init__(self):
        super().__init__(DataUtils.responses.session_expired_error)