from datetime import UTC, datetime
from typing import Any
from utils import DataUtils

from fastapi import Depends
from sqlalchemy import delete, asc, desc, inspect, select, update
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel

from db.base.base_db import BaseDB


class BaseRepository:
    def __init__(self, session: AsyncSession = Depends(BaseDB.get_session), model: type[SQLModel] | None = None):
        if model is None:
            model = getattr(self, "model", None)
            if not model:
                raise ValueError(DataUtils.responses.model_not_defined_error_message.format(class_name=self.__class__.__name__))

        self.session = session
        self.model = model
        self.db = BaseDB(session)

    async def get_all(self, target: dict | SQLModel | None = None, with_soft_deleted: bool = False) -> list[Any]:
        query = self.db.build_select_query(self.model, target or {}, with_soft_deleted)
        result = await self.session.execute(query.order_by(asc(self.model.id)))
        return result.scalars().all()

    async def get_first(self, target: dict | SQLModel, with_soft_deleted: bool) -> Any | None:
        query = self.db.build_select_query(self.model, target, with_soft_deleted)
        result = await self.session.execute(query.order_by(desc(self.model.id)).limit(1))
        return result.scalars().first()

    async def get_one_or_none(self, target: dict | SQLModel, with_soft_deleted: bool) -> Any | None:
        query = self.db.build_select_query(self.model, target, with_soft_deleted)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def get_all_with_joinedload(
        self, keys: list[str] | None = None, with_soft_deleted: bool = False, target: dict | SQLModel | None = None
    ) -> list[Any]:
        query = self.db.build_select_query_with_joinedload(self.model, target or {}, keys, with_soft_deleted)
        result = await self.session.execute(query.order_by(asc(self.model.id)))
        res = result.unique().scalars().all()

        if not with_soft_deleted:
            return self.model.clean_soft_deleted_relations(res)

        return res

    async def get_first_with_joinedload(
        self, target: dict | SQLModel, keys: list[str], with_soft_deleted: bool
    ) -> Any | None:
        query = self.db.build_select_query_with_joinedload(self.model, target, keys, with_soft_deleted)
        result = await self.session.execute(query.order_by(desc(self.model.id)).limit(1))
        res = result.unique().scalars().first()

        if res and not with_soft_deleted:
            return self.model.clean_soft_deleted_relations(res)

        return res

    async def get_one_or_none_with_joinedload(
        self, target: dict | SQLModel, keys: list[str], with_soft_deleted: bool
    ) -> Any | None:
        query = self.db.build_select_query_with_joinedload(self.model, target, keys, with_soft_deleted)
        result = await self.session.execute(query)
        res = result.unique().scalars().one_or_none()

        if res and not with_soft_deleted:
            return self.model.clean_soft_deleted_relations(res)

        return res

    async def create(self, instance: SQLModel) -> None:
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)

    async def update_one(self, target: dict, fields_to_update: dict, with_soft_deleted: bool = False) -> Any | None:
        query = self.db.build_select_query(self.model, target, with_soft_deleted)
        result = await self.session.execute(query)
        record = result.scalars().one_or_none()

        if record:
            for key, value in fields_to_update.items():
                setattr(record, key, value)

        await self.session.flush()
        return record

    async def update_all(self, target: dict, fields_to_update: dict, with_soft_deleted: bool = False) -> list[Any]:
        query = self.db.build_select_query(self.model, target, with_soft_deleted)
        result = await self.session.execute(query.order_by(asc(self.model.id)))
        records = result.scalars().all()

        for record in records:
            for key, value in fields_to_update.items():
                setattr(record, key, value)

        await self.session.flush()
        return records

    async def create_or_update(self, instance: SQLModel) -> None:
        instance_properties = dict(instance)
        instance_properties["updated_at"] = datetime.now(UTC)

        await self.session.execute(
            insert(self.model).values(**instance_properties).on_duplicate_key_update(**instance_properties)
        )

        await self.session.flush()

    async def seed(self, instances: list[SQLModel]) -> None:
        for index, instance in enumerate(instances):
            instance.id = index + 1
            await self.create_or_update(instance)

    async def delete(
        self,
        soft_delete: bool,
        target: dict | SQLModel | None = None,
    ) -> None:
        paths = self.get_relations()
        query = self.db.build_select_query_with_joinedload(self.model, target or {}, paths, with_soft_deleted=True)

        result = await self.session.execute(query)
        existing_records = result.unique().scalars().all()

        if existing_records:
            if soft_delete:
                current_time = datetime.now(UTC)
                for existing_record in existing_records:
                    existing_record.deleted_at = current_time
                    await self.db.cascade_soft_delete(existing_record, current_time)
            else:
                for existing_record in existing_records:
                    await self.session.delete(existing_record)

        await self.session.flush()

    async def bulk_delete(
        self,
        soft_delete: bool,
        target: dict | SQLModel | None = None,
    ) -> None:
        query = self.db.build_select_query(self.model, target or {}, with_soft_deleted=True)

        if soft_delete:
            current_time = datetime.now(UTC)
            result = await self.session.execute(select(self.model.id).where(query.whereclause))
            ids_to_delete = result.scalars().all()

            if not ids_to_delete:
                return

            for relationship in inspect(self.model).relationships:
                if relationship.cascade.delete or relationship.cascade.delete_orphan:
                    child_model = relationship.mapper.class_

                    for _local_col, remote_col in relationship.local_remote_pairs:
                        await self.session.execute(
                            update(child_model).where(remote_col.in_(ids_to_delete)).values(deleted_at=current_time)
                        )

            await self.session.execute(
                update(self.model).where(self.model.id.in_(ids_to_delete)).values(deleted_at=current_time)
            )
        else:
            await self.session.execute(delete(self.model).where(query.whereclause))

        await self.session.flush()

    def get_relations(self):
        paths = []

        def _scan(current_model, prefix=""):
            mapper = inspect(current_model)

            for rel in mapper.relationships:
                if rel.direction.name == "MANYTOONE":
                    continue

                path = f"{prefix}{rel.key}" if not prefix else f"{prefix}.{rel.key}"
                paths.append(path)
                _scan(rel.mapper.class_, path)

        _scan(self.model)
        return paths
