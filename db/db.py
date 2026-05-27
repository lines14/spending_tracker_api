from datetime import datetime
from sqlmodel import SQLModel
from typing import Type, Union
from sqlalchemy.sql import and_
from db.base.base_db import BaseDB 
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import desc, select, update, delete

class DB(BaseDB):
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
                            await db.session.close()  # На всякий случай закрываем или удаляем
                            await db.session.delete(existing_record)