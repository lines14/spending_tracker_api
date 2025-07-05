from typing import ClassVar
from utils.data_utils import DataUtils
from pydantic import Field, model_validator
from DTO.base import BaseDTO, StringValidator

class UserDTO(BaseDTO):
    max_length: ClassVar[int] = 20
    login_min_length: ClassVar[int] = 4
    password_min_length: ClassVar[int] = 6

    login: str = Field(
        default=..., 
        description=DataUtils.responses.login_validation_message, 
        min_length=login_min_length, 
        max_length=max_length
    )

    password: str = Field(
        default=..., 
        description=DataUtils.responses.password_validation_message, 
        min_length=password_min_length, 
        max_length=max_length
    )

    @model_validator(mode="after")
    @classmethod
    def validate_fields(cls, values):
        login = StringValidator(values.login)
        password = StringValidator(values.password)

        if (not login.is_length_between(cls.login_min_length, cls.max_length) 
            or not login.is_alphanumeric() or login.has_spaces()):
            raise ValueError(DataUtils.responses.login_validation_message)
        
        if (not password.is_length_between(cls.password_min_length, cls.max_length) 
            or not password.is_alphanumeric() or password.has_spaces()):
            raise ValueError(DataUtils.responses.password_validation_message)
        
        return values