import re
from typing import Any

from fastapi import HTTPException, Request
from pydantic import BaseModel, ConfigDict, ValidationError, create_model
from sqlalchemy import inspect
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
            result = []
            for item in obj:
                if getattr(item, "deleted_at", None) is None:
                    item_dict = cls.nested_models_to_dict(item)
                    cleaned_dict = cls._clean_soft_deleted_records(item_dict)
                    result.append(cls._build_model(cls, cleaned_dict))

            return result

        if not isinstance(obj, SQLModel):
            return obj

        if getattr(obj, "deleted_at", None) is not None:
            return None

        obj_dict = cls.nested_models_to_dict(obj)
        cleaned_dict = cls._clean_soft_deleted_records(obj_dict)

        return cls._build_model(cls, cleaned_dict)

    @classmethod
    def _clean_soft_deleted_records(cls, node):
        if isinstance(node, dict):
            out = {}
            for key, value in node.items():
                if isinstance(value, dict):
                    if value.get("deleted_at") is None:
                        out[key] = cls._clean_soft_deleted_records(value)
                elif isinstance(value, list):
                    processed_list = []
                    for item in value:
                        if isinstance(item, dict):
                            if item.get("deleted_at") is None:
                                processed_list.append(cls._clean_soft_deleted_records(item))
                        else:
                            processed_list.append(item)
                    out[key] = processed_list
                else:
                    out[key] = value
            return out

        if isinstance(node, list):
            return [cls._clean_soft_deleted_records(index) for index in node]

        return node

    @classmethod
    def _build_model(cls, model_cls, data):
        relationships = {relationship.key: relationship for relationship in inspect(model_cls).relationships}
        kwargs = {}
        for key, value in data.items():
            if key in relationships and value is not None:
                relationship = relationships[key]
                child_cls = relationship.mapper.class_
                if relationship.uselist:
                    kwargs[key] = [cls._build_model(child_cls, it) if isinstance(it, dict) else it for it in value]
                else:
                    kwargs[key] = cls._build_model(child_cls, value) if isinstance(value, dict) else value
            else:
                kwargs[key] = value

        return model_cls(**kwargs)

    @classmethod
    def nested_models_to_dict(cls, obj: SQLModel | list[SQLModel] | dict | Any, visited = None) -> Any:
        if visited is None:
            visited = set()

        if isinstance(obj, list):
            return [cls.nested_models_to_dict(item, visited) for item in obj]

        if isinstance(obj, SQLModel):
            object_id = id(obj)
            if object_id in visited:
                return {"id": getattr(obj, "id", None)}

            visited.add(object_id)

            result = {}
            for key, value in obj.__dict__.items():
                if key.startswith("_"):
                    continue

                result[key] = cls.nested_models_to_dict(value, visited)

            return result

        if isinstance(obj, dict):
            return {key: cls.nested_models_to_dict(value, visited) for key, value in obj.items()}

        return obj
