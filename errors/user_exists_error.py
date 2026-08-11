from errors.base.base_custom_error import BaseCustomError
from utils import DataUtils


class UserExistsError(BaseCustomError):
    def __init__(self):
        super().__init__(DataUtils.responses.user_exists_error)
