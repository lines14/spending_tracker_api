from collections.abc import AsyncGenerator
from datetime import datetime

from sqlalchemy import inspect, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import and_
from sqlmodel import SQLModel

from config import Config


class BaseDB:
    engine = create_async_engine(Config().db_url_async, pool_pre_ping=True)

    sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)

    def __init__(self, session: AsyncSession | None = None):
        self.session = session

    async def __aenter__(self):
        if not self.session:
            self.session = self.sessionmaker()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session and self.session.is_active:
            if exc_type is not None:
                await self.session.rollback()
            else:
                await self.session.commit()
            await self.session.close()

    @classmethod
    async def get_session(cls) -> AsyncGenerator[AsyncSession, None]:
        async with cls.sessionmaker() as session:
            try:
                yield session

                if session.is_active:
                    await session.commit()
            except Exception:
                if session.is_active:
                    await session.rollback()
                raise

    @classmethod
    async def dispose_engine(cls):
        await cls.engine.dispose()

    async def init_tables(self):
        async with self.engine.begin() as connection:
            await connection.run_sync(SQLModel.metadata.create_all)

    @staticmethod
    def build_nested_joinedload(model: type[SQLModel], key: str):
        parts = key.split(".")
        loader = joinedload(getattr(model, parts[0]))
        current_model = model.__mapper__.relationships[parts[0]].mapper.class_

        for part in parts[1:]:
            loader = loader.joinedload(getattr(current_model, part))
            current_model = current_model.__mapper__.relationships[part].mapper.class_

        return loader

    def get_not_empty_properties(self, instance):
        instance_properties = {attr.key: getattr(instance, attr.key) for attr in inspect(instance).mapper.column_attrs}

        return {key: value for key, value in instance_properties.items() if value is not None}

    def get_filter_expressions(self, model: type[SQLModel], target: dict | SQLModel):
        filter_expressions = []

        instance_properties = target if isinstance(target, dict) else self.get_not_empty_properties(target)

        if "id" in instance_properties and instance_properties["id"] is not None:
            value = instance_properties["id"]
            if isinstance(value, (list, tuple, set)):
                return [model.id.in_(value)]
            return [model.id == value]

        for key, value in instance_properties.items():
            if value is not None:
                if isinstance(value, (list, tuple, set)):
                    filter_expressions.append(getattr(model, key).in_(value))
                else:
                    filter_expressions.append(getattr(model, key) == value)

        return filter_expressions

    def build_select_query(
        self, model: type[SQLModel], target: dict | SQLModel, with_soft_deleted: bool, load_all: bool = False
    ):
        filter_expressions = self.get_filter_expressions(model, target)

        if not with_soft_deleted and hasattr(model, "deleted_at"):
            filter_expressions.append(model.deleted_at.is_(None))

        query = select(model).where(and_(*filter_expressions))

        if load_all:
            for rel in inspect(model).relationships:
                query = query.options(joinedload(getattr(model, rel.key)))

        return query

    def build_select_query_with_joinedload(
        self, model: type[SQLModel], target: dict | SQLModel, keys: list[str], with_soft_deleted: bool = False
    ):
        query = self.build_select_query(model, target, with_soft_deleted)
        options = [self.build_nested_joinedload(model, key) for key in keys]
        return query.options(*options)

    async def cascade_soft_delete(self, parent_record, current_time: datetime) -> None:
        mapper = inspect(parent_record.__class__)
        for relationship in mapper.relationships:
            if relationship.cascade.delete or relationship.cascade.delete_orphan:
                related_value = getattr(parent_record, relationship.key)
                if not related_value:
                    continue

                if isinstance(related_value, list):
                    for child in related_value:
                        if hasattr(child, "deleted_at") and child.deleted_at is None:
                            child.deleted_at = current_time
                            await self.cascade_soft_delete(child, current_time)

                else:
                    if hasattr(related_value, "deleted_at") and related_value.deleted_at is None:
                        related_value.deleted_at = current_time
                        await self.cascade_soft_delete(related_value, current_time)
