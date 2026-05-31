from config import Config
from sqlmodel import SQLModel
from datetime import datetime
from typing import Type, Union
from sqlalchemy.sql import and_
from sqlalchemy.orm import joinedload
from sqlalchemy import inspect, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

class BaseDB:
    engine = create_async_engine(Config().DB_URL_ASYNC)

    sessionmaker = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False
    )

    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = self.sessionmaker()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    @classmethod
    async def dispose_engine(cls):
        await cls.engine.dispose()

    async def init_tables(self):
        async with self.engine.begin() as connection:
            await connection.run_sync(SQLModel.metadata.create_all)

    @staticmethod
    def build_nested_joinedload(model: Type[SQLModel], key: str):
        parts = key.split(".")
        loader = joinedload(getattr(model, parts[0]))
        current_model = model.__mapper__.relationships[parts[0]].mapper.class_

        for part in parts[1:]:
            loader = loader.joinedload(getattr(current_model, part))
            current_model = current_model.__mapper__.relationships[part].mapper.class_

        return loader
    
    def get_not_empty_properties(self, instance):
        instance_properties = {
            attr.key: getattr(instance, attr.key)
            for attr in inspect(instance).mapper.column_attrs
        }
        return {key: value for key, value in instance_properties.items() if value is not None}
    
    def get_filter_expressions(self, model: Type[SQLModel], target: Union[dict, SQLModel]):
        filter_expressions = []

        if isinstance(target, dict):
            instance_properties = target
        else:
            instance_properties = self.get_not_empty_properties(target)

        if 'id' in instance_properties and instance_properties['id'] is not None:
            value = instance_properties['id']
            if isinstance(value, (list, tuple, set)):
                return [getattr(model, 'id').in_(value)]
            else:
                return [getattr(model, 'id') == value]

        for key, value in instance_properties.items():
            if value is not None:
                if isinstance(value, (list, tuple, set)):
                    filter_expressions.append(getattr(model, key).in_(value))
                else:
                    filter_expressions.append(getattr(model, key) == value)

        return filter_expressions
    
    def build_select_query(
        self, 
        model: Type[SQLModel], 
        target: Union[dict, SQLModel], 
        with_soft_deleted: bool,
        load_all: bool = False
    ):
        filter_expressions = self.get_filter_expressions(model, target)

        if not with_soft_deleted and hasattr(model, 'deleted_at'):
            filter_expressions.append(getattr(model, 'deleted_at') == None)

        query = select(model).where(and_(*filter_expressions))

        if load_all:
            for rel in inspect(model).relationships:
                query = query.options(joinedload(getattr(model, rel.key)))
                
        return query
    
    def build_select_query_with_joinedload(
        self, 
        model: Type[SQLModel], 
        target: Union[dict, SQLModel], 
        keys: list[str],
        with_soft_deleted: bool = False
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
                        if hasattr(child, 'deleted_at') and child.deleted_at is None:
                            setattr(child, 'deleted_at', current_time)
                            await self.cascade_soft_delete(child, current_time)
                
                else:
                    if hasattr(related_value, 'deleted_at') and related_value.deleted_at is None:
                        setattr(related_value, 'deleted_at', current_time)
                        await self.cascade_soft_delete(related_value, current_time)