import re
from db.db import DB
from typing import Optional
from sqlalchemy import func
from pydantic import ConfigDict
from typing import Type, Union, Any
from datetime import datetime, timezone
from sqlalchemy.orm import declared_attr
from fastapi import HTTPException, Request
from fastapi.exceptions import HTTPException
from sqlmodel import SQLModel, TIMESTAMP, Field
from pydantic import BaseModel, ValidationError, create_model

class BaseModel(SQLModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True
    )
    
    id: int = Field(primary_key=True, nullable=False)

    created_at: datetime = Field(
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={"server_default": func.now()},
        nullable=False,
    )

    updated_at: datetime = Field(
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={
            "onupdate": lambda: datetime.now(timezone.utc), 
            "server_default": func.now()
        },
        nullable=False,
    )

    deleted_at: Optional[datetime] = Field(
        sa_type=TIMESTAMP(timezone=True),
        nullable=True,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower() + 's'

    async def create(self) -> None:
        await DB().create(self)

    async def get(self, with_soft_deleted: bool = False) -> list[SQLModel]:
        return await DB().get(type(self), self, with_soft_deleted)
    
    async def get_with_joined_load(
        self, 
        keys: list[str], 
        with_soft_deleted: bool = False
    ) -> list[SQLModel]:
        result = await DB().get_with_joined_load(self, keys, with_soft_deleted)

        if not with_soft_deleted:
            return self.clean_soft_deleted_relations(result)
    
        return result

    async def update(self) -> list[SQLModel]:
        return await DB().update(
            type(self),
            self.model_dump(exclude_unset=True),
            self.model_dump(exclude_unset=True)
        )

    async def delete(self, soft_delete: bool = True) -> None:
        await DB().delete(type(self), self, soft_delete)

    @classmethod
    async def bulk_get(cls, search_by: dict, with_soft_deleted: bool = False) -> list[SQLModel]:
        return await DB().get(cls, search_by, with_soft_deleted)
    
    @classmethod
    async def bulk_get_with_joined_load(
        cls, 
        search_by: dict, 
        keys: list[str], 
        with_soft_deleted: bool = False
    ) -> list[SQLModel]:
        result = await DB().get_with_joined_load(cls, search_by, keys, with_soft_deleted)

        if not with_soft_deleted:
            return cls.clean_soft_deleted_relations(result)
    
        return result

    @classmethod
    async def bulk_update(cls, search_by: dict, fields_to_update: dict) -> list[SQLModel]:
        return await DB().update(cls, search_by, fields_to_update)
    
    @classmethod
    async def bulk_delete(cls, search_by: dict, soft_delete: bool = True) -> None:
        await DB().delete(cls, search_by, soft_delete)

    @classmethod
    def validate(cls: Type[BaseModel], fields: list[str]):
        async def validate_fields(request: Request) -> BaseModel:
            errors = []
            validated_data = {}
            
            data = await request.json()

            for field in fields:
                if field in data:
                    try:
                        SingleFieldModel = create_model(
                            'SingleFieldModel', 
                            **{field: (cls.__annotations__[field], ...)}
                        )

                        validated_field = SingleFieldModel(**{field: data[field]})
                        validated_data[field] = validated_field.dict()[field]
                    except ValidationError as e:
                        errors.extend(e.errors())
                else:
                    errors.append({
                        "type": "missing",
                        "loc": ["body", field],
                        "msg": "Field required",
                        "input": None
                    })

            if errors:
                raise HTTPException(422, detail=errors)
            
            return cls(**validated_data)
        
        return validate_fields
    
    @classmethod
    def clean_soft_deleted_relations(cls, obj: Union[SQLModel, list[SQLModel]]):
        if isinstance(obj, list):
            return [cls.clean_soft_deleted_relations(item) 
                    for item in obj if item.deleted_at is None]

        if not isinstance(obj, SQLModel):
            return obj

        for key, value in obj.__dict__.items():
            if isinstance(value, list):
                cleaned = [val for val in value if isinstance(val, SQLModel) 
                           and getattr(val, "deleted_at", None) is None]

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
    def nested_models_to_dict(cls, obj: Union[SQLModel, list[SQLModel], dict, Any]) -> Any:
        if isinstance(obj, list):
            return [cls.nested_models_to_dict(item) for item in obj]

        elif isinstance(obj, SQLModel):
            result = {}

            for key, value in obj.__dict__.items():
                if key.startswith("_"):
                    continue

                result[key] = cls.nested_models_to_dict(value)

            return result

        elif isinstance(obj, dict):
            return {key: cls.nested_models_to_dict(value) for key, value in obj.items()}

        else:
            return obj