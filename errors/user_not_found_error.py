from errors.base.base_custom_error import BaseCustomError
from utils import DataUtils


class UserNotFoundError(BaseCustomError):
    def __init__(self):
        super().__init__(DataUtils.responses.user_not_found_error)
