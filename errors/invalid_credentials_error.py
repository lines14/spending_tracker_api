from errors.base.base_custom_error import BaseCustomError
from utils import DataUtils


class InvalidCredentialsError(BaseCustomError):
    def __init__(self):
        super().__init__(DataUtils.responses.invalid_credentials_error)
