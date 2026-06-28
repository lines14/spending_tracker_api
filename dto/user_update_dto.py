from typing import Optional, ClassVar
from utils.data_utils import DataUtils
from pydantic import Field, model_validator
from dto.base import BaseDTO, StringValidator

class UserUpdateDTO(BaseDTO):
    max_length: ClassVar[int] = 20
    login_min_length: ClassVar[int] = 4
    password_min_length: ClassVar[int] = 6

    id: Optional[int] = None

    login: Optional[str] = Field(
        default=None,
        description=DataUtils.responses.login_validation_message,
        min_length=login_min_length,
        max_length=max_length
    )

    password: Optional[str] = Field(
        default=None,
        description=DataUtils.responses.password_validation_message,
        min_length=password_min_length,
        max_length=max_length
    )

    hashed_password: Optional[str] = None

    @model_validator(mode="after")
    @classmethod
    def validate_fields(cls, values):
        if values.login is not None:
            login = StringValidator(values.login)
            if (not login.is_length_between(cls.login_min_length, cls.max_length)
                or not login.is_alphanumeric() or login.has_spaces()):
                raise ValueError(DataUtils.responses.login_validation_message)

        if values.password is not None:
            password = StringValidator(values.password)
            if (not password.is_length_between(cls.password_min_length, cls.max_length)
                or not password.is_alphanumeric() or password.has_spaces()):
                raise ValueError(DataUtils.responses.password_validation_message)

        return values