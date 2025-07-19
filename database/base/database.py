from config import Config
from datetime import datetime
from sqlmodel import SQLModel
from typing import Type, Union
from sqlalchemy.sql import and_
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import DeclarativeBase, joinedload
from sqlalchemy import desc, select, update, delete, inspect
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

class Database(DeclarativeBase):
    # if sqlite add arg: connect_args={'check_same_thread': False}
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
            await connection.run_sync(self.metadata.create_all)

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

    async def create(self, instance: SQLModel):
        async with self as db:
            async with db.session.begin():
                db.session.add(instance)

            await db.session.refresh(instance)

    async def update(
        self, 
        model: Type[SQLModel], 
        filters: dict, 
        fields_to_update: dict
    ) -> list[SQLModel]:
        async with self as db:
            records = []
            updated_objects = []

            max_updates = max(len(value) if isinstance(value, list) else 1 
                              for value in {**filters, **fields_to_update}.values())

            for i in range(max_updates):
                record_filter = {}
                record_update = {}

                for key, value in filters.items():
                    if isinstance(value, list):
                        record_filter[key] = value[i] if i < len(value) else None
                    else:
                        record_filter[key] = value

                for key, value in fields_to_update.items():
                    if isinstance(value, list):
                        if i < len(value):
                            record_update[key] = value[i]
                    else:
                        record_update[key] = value

                if all(v is not None for v in record_filter.values()):
                    records.append((record_filter, record_update))

            async with db.session.begin():
                for record_filter, record_update in records:
                    filter_expressions = self.get_filter_expressions(model, record_filter)

                    result = await db.session.execute(
                        select(model)
                        .where(and_(*filter_expressions))
                    )

                    existing_records = result.scalars().all()

                    for existing_record in existing_records:
                        for key, value in record_update.items():
                            setattr(existing_record, key, value)

                        updated_objects.append(existing_record)

            return updated_objects

    async def create_or_update(self, instance: SQLModel):
        async with self as db:
            instance_properties = dict(instance)
            instance_properties['updated_at'] = datetime.utcnow()

            async with db.session.begin():
                await db.session.execute(
                    insert(type(instance))
                    .values(**instance_properties)
                    .on_duplicate_key_update(**instance_properties)
                )

    async def seed(self, instances: list[SQLModel]):
        async with self as db:
            for index, instance in enumerate(instances):
                instance.id = index + 1
                await db.create_or_update(instance)

    async def get(
        self, 
        model: Type[SQLModel], 
        target: Union[dict, SQLModel], 
        with_soft_deleted: bool
    ) -> list[SQLModel]:
        async with self as db:
            filter_expressions = self.get_filter_expressions(model, target)

            if not with_soft_deleted:
                filter_expressions.append(getattr(model, 'deleted_at') == None)

            result = await db.session.execute(
                select(model)
                .where(and_(*filter_expressions))
                .order_by(desc(model.id))
            )

            return result.scalars().all()

    async def get_with_joined_load(
        self, 
        model: Type[SQLModel], 
        target: Union[dict, SQLModel], 
        keys: list[str], 
        with_soft_deleted: bool
    ) -> list[SQLModel]:
        async with self as db:
            filter_expressions = self.get_filter_expressions(model, target)

            if not with_soft_deleted:
                filter_expressions.append(getattr(model, 'deleted_at') == None)

            options = [self.build_nested_joinedload(model, key) for key in keys]

            result = await db.session.execute(
                select(model)
                .options(*options)
                .where(and_(*filter_expressions))
                .order_by(desc(model.id))
            )

            return result.unique().scalars().all()
            
    async def execute_delete(
        self, 
        model: Type[SQLModel], 
        target: Union[dict, SQLModel], 
        soft_delete: bool
    ) -> None:
        async with self as db:
            filter_expressions = self.get_filter_expressions(model, target)

            async with db.session.begin():
                if soft_delete:
                    await db.session.execute(
                        update(model)
                        .where(and_(*filter_expressions))
                        .values(deleted_at=datetime.utcnow())
                    )
                else:
                    await db.session.execute(
                        delete(model)
                        .where(and_(*filter_expressions))
                    )

    async def delete(
        self, 
        model: Type[SQLModel], 
        target: Union[dict, SQLModel], 
        soft_delete: bool
    ) -> None:
        async with self as db:
            filter_expressions = self.get_filter_expressions(model, target)

            async with db.session.begin():
                result = await db.session.execute(
                    select(model)
                    .where(and_(*filter_expressions))
                )
                
                existing_records = result.scalars().all()

                if len(existing_records) > 0:
                    if soft_delete:
                        for existing_record in existing_records:
                            setattr(existing_record, 'deleted_at', datetime.utcnow())
                    else:
                        for existing_record in existing_records:
                            await db.session.delete(existing_record)