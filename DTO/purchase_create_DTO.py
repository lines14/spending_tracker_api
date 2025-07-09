from typing import ClassVar
from utils.data_utils import DataUtils
from pydantic import Field, model_validator
from DTO.base import BaseDTO, FloatValidator, IntegerValidator

class PurchaseCreateDTO(BaseDTO):
    cost_min_value: ClassVar[int] = 0.01
    cost_max_value: ClassVar[int] = 10000000
    sub_type_id_min_value: ClassVar[int] = 1
    sub_type_id_max_value: ClassVar[int] = 108

    cost: float = Field(
        default=..., 
        description=DataUtils.responses.cost_validation_message,
        ge=cost_min_value, 
        le=cost_max_value
    )

    account_id: int = Field(
        default=..., 
        description=DataUtils.responses.account_id_validation_message
    )

    sub_type_id: int = Field(
        default=..., 
        description=DataUtils.responses.sub_type_id_validation_message,
        ge=sub_type_id_min_value, 
        le=sub_type_id_max_value
    )

    @model_validator(mode="after")
    @classmethod
    def validate_fields(cls, values):
        cost = FloatValidator(values.cost)
        sub_type_id = IntegerValidator(values.sub_type_id)

        if (not cost.has_two_decimal_places() 
            and not cost.is_in_range(cls.cost_min_value, cls.cost_max_value)):
            raise ValueError(DataUtils.responses.cost_validation_message)
        
        if not sub_type_id.is_in_range(cls.sub_type_id_min_value, cls.sub_type_id_max_value):
            raise ValueError(DataUtils.responses.sub_type_id_validation_message)
        
        return values