import re
from typing import Any

from fastapi import HTTPException, Request
from pydantic import BaseModel, ConfigDict, ValidationError, create_model
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )

    id: int = Field(primary_key=True, nullable=False)

    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa: N805
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower() + "s"

    @classmethod
    def validate(cls: type[BaseModel], fields: list[str]):
        async def validate_fields(request: Request) -> BaseModel:
            errors = []
            validated_data = {}

            data = await request.json()

            for field in fields:
                if field in data:
                    try:
                        single_field_model = create_model(
                            "SingleFieldModel", **{field: (cls.__annotations__[field], ...)}
                        )

                        validated_field = single_field_model(**{field: data[field]})
                        validated_data[field] = validated_field.dict()[field]
                    except ValidationError as e:
                        errors.extend(e.errors())
                else:
                    errors.append({"type": "missing", "loc": ["body", field], "msg": "Field required", "input": None})

            if errors:
                raise HTTPException(422, detail=errors)

            return cls(**validated_data)

        return validate_fields

    @classmethod
    def clean_soft_deleted_relations(cls, obj: SQLModel | list[SQLModel]):
        if isinstance(obj, list):
            return [cls.clean_soft_deleted_relations(item) for item in obj if item.deleted_at is None]

        if not isinstance(obj, SQLModel):
            return obj

        for key, value in obj.__dict__.items():
            if isinstance(value, list):
                cleaned = [
                    val for val in value if isinstance(val, SQLModel) and getattr(val, "deleted_at", None) is None
                ]

                for item in cleaned:
                    cls.clean_soft_deleted_relations(item)

                setattr(obj, key, cleaned)
            elif isinstance(value, SQLModel):
                if getattr(value, "deleted_at", None) is not None:
                    setattr(obj, key, None)
                else:
                    cls.clean_soft_deleted_relations(value)

        return obj

    @classmethod
    def nested_models_to_dict(cls, obj: SQLModel | list[SQLModel] | dict | Any) -> Any:
        if isinstance(obj, list):
            return [cls.nested_models_to_dict(item) for item in obj]

        if isinstance(obj, SQLModel):
            result = {}

            for key, value in obj.__dict__.items():
                if key.startswith("_"):
                    continue

                result[key] = cls.nested_models_to_dict(value)

            return result

        if isinstance(obj, dict):
            return {key: cls.nested_models_to_dict(value) for key, value in obj.items()}

        return obj
