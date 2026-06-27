import re
from pydantic import ConfigDict
from db.base.base_db import BaseDB
from sqlmodel import Field, SQLModel
from datetime import datetime, timezone
from sqlalchemy.orm import declared_attr
from sqlalchemy.dialects.mysql import insert
from typing import Any, Optional, Union, ClassVar
from sqlalchemy import delete, desc, inspect, select, update

class BaseModel(SQLModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )

    id: int = Field(primary_key=True, nullable=False)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower() + "s"

    @classmethod
    @property
    def model(cls) -> ClassVar[Any]:
        return cls

    @classmethod
    async def get_all(
        cls,
        target: Optional[Union[dict, SQLModel]] = None,
        with_soft_deleted: bool = False,
    ) -> list[Any]:
        async with BaseDB() as db:
            query = db.build_select_query(cls.model, target or {}, with_soft_deleted)
            result = await db.session.execute(
                query.order_by(desc(cls.model.id))
            )

            return result.scalars().all()

    @classmethod
    async def get_first(
        cls, 
        target: Union[dict, SQLModel], 
        with_soft_deleted: bool = False
    ) -> Optional[Any]:
        async with BaseDB() as db:
            query = db.build_select_query(cls.model, target, with_soft_deleted)
            result = await db.session.execute(query.order_by(desc(cls.model.id)).limit(1))

            return result.scalars().first()

    @classmethod
    async def get_one_or_none(
        cls, 
        target: Union[dict, SQLModel], 
        with_soft_deleted: bool = False
    ) -> Optional[Any]:
        async with BaseDB() as db:
            query = db.build_select_query(cls.model, target, with_soft_deleted)
            result = await db.session.execute(query)

            return result.scalars().one_or_none()

    @classmethod
    async def get_all_with_joinedload(
        cls,
        keys: list[str] = None,
        with_soft_deleted: bool = False,
        target: Optional[Union[dict, SQLModel]] = None,
    ) -> list[Any]:
        async with BaseDB() as db:
            query = db.build_select_query_with_joinedload(cls.model, target or {}, keys, with_soft_deleted)
            result = await db.session.execute(query.order_by(desc(cls.model.id)))
            res = result.unique().scalars().all()

            if not with_soft_deleted:
                return cls.model.clean_soft_deleted_relations(res)

            return res

    @classmethod
    async def get_first_with_joinedload(
        cls,
        target: Union[dict, SQLModel],
        keys: list[str],
        with_soft_deleted: bool = False,
    ) -> Optional[Any]:
        async with BaseDB() as db:
            query = db.build_select_query_with_joinedload(cls.model, target, keys, with_soft_deleted)
            result = await db.session.execute(query.order_by(desc(cls.model.id)).limit(1))
            res = result.unique().scalars().first()

            if res and not with_soft_deleted:
                return cls.model.clean_soft_deleted_relations(res)

            return res

    @classmethod
    async def get_one_or_none_with_joinedload(
        cls,
        target: Union[dict, SQLModel],
        keys: list[str],
        with_soft_deleted: bool = False,
    ) -> Optional[Any]:
        async with BaseDB() as db:
            query = db.build_select_query_with_joinedload(cls.model, target, keys, with_soft_deleted)
            result = await db.session.execute(query)
            res = result.unique().scalars().one_or_none()

            if res and not with_soft_deleted:
                return cls.model.clean_soft_deleted_relations(res)

            return res

    async def create(self) -> None:
        async with BaseDB() as db:
            async with db.session.begin():
                db.session.add(self)
            await db.session.refresh(self)

    @classmethod
    async def update_one(
        cls, 
        target: dict, 
        fields_to_update: dict
    ) -> Optional[Any]:
        async with BaseDB() as db:
            async with db.session.begin():
                query = db.build_select_query(cls.model, target, with_soft_deleted=False)
                result = await db.session.execute(query)
                record = result.scalars().one_or_none()

                if record:
                    for key, value in fields_to_update.items():
                        setattr(record, key, value)

                return record

    @classmethod
    async def update_all(
        cls, 
        target: dict, 
        fields_to_update: dict
    ) -> list[Any]:
        async with BaseDB() as db:
            async with db.session.begin():
                query = db.build_select_query(cls.model, target, with_soft_deleted=False)
                result = await db.session.execute(query.order_by(desc(cls.model.id)))
                records = result.scalars().all()

                for record in records:
                    for key, value in fields_to_update.items():
                        setattr(record, key, value)

                return records

    @classmethod
    async def create_or_update(cls, instance: SQLModel) -> None:
        async with BaseDB() as db:
            instance_properties = dict(instance)
            instance_properties["updated_at"] = datetime.now(timezone.utc)

            async with db.session.begin():
                await db.session.execute(
                    insert(cls.model)
                    .values(**instance_properties)
                    .on_duplicate_key_update(**instance_properties)
                )

    @classmethod
    async def seed(cls, instances: list[SQLModel]) -> None:
        for index, instance in enumerate(instances):
            instance.id = index + 1
            await cls.create_or_update(instance)

    @classmethod
    async def delete(
        cls,
        soft_delete: bool,
        target: Optional[Union[dict, SQLModel]] = None,
    ) -> None:
        async with BaseDB() as db:
            async with db.session.begin():
                paths = cls.get_relations()
                query = db.build_select_query_with_joinedload(
                    cls.model, target or {}, paths, with_soft_deleted=True
                )

                result = await db.session.execute(query)
                existing_records = result.unique().scalars().all()

                if existing_records:
                    if soft_delete:
                        current_time = datetime.now(timezone.utc)
                        for existing_record in existing_records:
                            setattr(existing_record, "deleted_at", current_time)
                            await db.cascade_soft_delete(existing_record, current_time)
                    else:
                        for existing_record in existing_records:
                            await db.session.delete(existing_record)

    @classmethod
    async def bulk_delete(
        cls,
        soft_delete: bool,
        target: Optional[Union[dict, SQLModel]] = None,
    ) -> None:
        async with BaseDB() as db:
            async with db.session.begin():
                query = db.build_select_query(cls.model, target or {}, with_soft_deleted=True)

                if soft_delete:
                    current_time = datetime.now(timezone.utc)
                    result = await db.session.execute(select(cls.model.id).where(query.whereclause))
                    ids_to_delete = result.scalars().all()

                    if not ids_to_delete:
                        return

                    for relationship in inspect(cls.model).relationships:
                        if relationship.cascade.delete or relationship.cascade.delete_orphan:
                            child_model = relationship.mapper.class_

                            for local_col, remote_col in relationship.local_remote_pairs:
                                await db.session.execute(
                                    update(child_model)
                                    .where(remote_col.in_(ids_to_delete))
                                    .values(deleted_at=current_time)
                                )

                    await db.session.execute(
                        update(cls.model)
                        .where(cls.model.id.in_(ids_to_delete))
                        .values(deleted_at=current_time)
                    )
                else:
                    await db.session.execute(
                        delete(cls.model)
                        .where(query.whereclause)
                    )

    @classmethod
    def get_relations(cls):
        paths = []

        def _scan(current_model, prefix=""):
            mapper = inspect(current_model)

            for rel in mapper.relationships:
                if rel.direction.name == "MANYTOONE":
                    continue

                path = f"{prefix}{rel.key}" if not prefix else f"{prefix}.{rel.key}"
                paths.append(path)
                _scan(rel.mapper.class_, path)

        _scan(cls.model)
        return paths

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