import re
from sqlmodel import Field
from sqlalchemy import func
from typing import Type, List
from datetime import datetime, timezone
from sqlmodel import SQLModel, TIMESTAMP
from sqlalchemy.orm import declared_attr
from fastapi import HTTPException, Request
from database.base.database import Database
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, ValidationError, create_model

class BaseModel(SQLModel):
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

    deleted_at: datetime = Field(
        sa_type=TIMESTAMP(timezone=True),
        nullable=True,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower() + 's'

    async def create(self):
        await Database().create(self)

    async def delete(self, soft_delete: bool = True):
        await Database().delete(self, soft_delete)

    async def get(self, with_soft_deleted: bool = False):
        return await Database().get(self, with_soft_deleted)
        
    async def get_all(self, with_soft_deleted: bool = False):
        return await Database().get_all(self, with_soft_deleted)

    @classmethod
    def validate(cls: Type[BaseModel], fields: List[str]):
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

    class Config:
        from_attributes = True
        validate_assignment = True
        arbitrary_types_allowed=True