from typing import ClassVar
from utils.data_utils import DataUtils
from pydantic import Field, model_validator
from DTO.base import BaseDTO, IntegerValidator, StringValidator

class BankAccountCreateDTO(BaseDTO):
    account_min_length: ClassVar[int] = 4
    account_max_length: ClassVar[int] = 20
    issuer_id_min_value: ClassVar[int] = 1
    issuer_id_max_value: ClassVar[int] = 11
    currency_id_min_value: ClassVar[int] = 1
    currency_id_max_value: ClassVar[int] = 4

    account: str = Field(
        default=..., 
        description=DataUtils.responses.account_validation_message,
        min_length=account_min_length, 
        max_length=account_max_length
    )

    issuer_id: int = Field(
        default=..., 
        description=DataUtils.responses.issuer_id_validation_message,
        ge=issuer_id_min_value, 
        le=issuer_id_max_value
    )

    currency_id: int = Field(
        default=..., 
        description=DataUtils.responses.currency_id_validation_message,
        ge=currency_id_min_value, 
        le=currency_id_max_value
    )

    user_id: int = Field(
        default=..., 
        description=DataUtils.responses.user_id_validation_message
    )

    @model_validator(mode="after")
    @classmethod
    def validate_fields(cls, values):
        account = StringValidator(values.account)
        issuer_id = IntegerValidator(values.issuer_id)
        currency_id = IntegerValidator(values.currency_id)

        if (not account.is_length_between(cls.account_min_length, cls.account_max_length) 
            or not account.is_alphanumeric_with_spaces()):
            raise ValueError(DataUtils.responses.account_validation_message)
        
        if not issuer_id.is_in_range(cls.issuer_id_min_value, cls.issuer_id_max_value):
            raise ValueError(DataUtils.responses.issuer_id_validation_message)
        
        if not currency_id.is_in_range(cls.currency_id_min_value, cls.currency_id_max_value):
            raise ValueError(DataUtils.responses.currency_id_validation_message)
        
        return values