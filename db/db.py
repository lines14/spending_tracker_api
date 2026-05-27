from datetime import datetime
from sqlmodel import SQLModel
from db.base.base_db import BaseDB 
from typing import Type, Union, Optional
from sqlalchemy import desc, update, delete
from sqlalchemy.dialects.mysql import insert

class DB(BaseDB):
    async def get_all(
        self, 
        model: Type[SQLModel], 
        target: Union[dict, SQLModel], 
        with_soft_deleted: bool = False
    ) -> list[SQLModel]:
        async with self as db:
            query = self.build_select_query(model, target, with_soft_deleted)
            result = await db.session.execute(query.order_by(desc(model.id)))
            return result.scalars().all()
        
    async def get_first(
        self, 
        model: Type[SQLModel], 
        target: Union[dict, SQLModel],
        with_soft_deleted: bool = False
    ) -> Optional[SQLModel]:
        async with self as db:
            query = self.build_select_query(model, target, with_soft_deleted)
            result = await db.session.execute(query.order_by(desc(model.id)).limit(1))
            return result.scalars().first()
        
    async def get_one_or_none(
        self, 
        model: Type[SQLModel], 
        target: Union[dict, SQLModel], 
        with_soft_deleted: bool = False
    ) -> Optional[SQLModel]:
        async with self as db:
            query = self.build_select_query(model, target, with_soft_deleted)
            result = await db.session.execute(query)
            return result.scalars().one_or_none()

    async def get_all_with_joinedload(
        self, 
        model: Type[SQLModel], 
        target: Union[dict, SQLModel], 
        keys: list[str], 
        with_soft_deleted: bool = False
    ) -> list[SQLModel]:
        async with self as db:
            query = self.build_select_query_with_joinedload(model, target, keys, with_soft_deleted)
            result = await db.session.execute(query.order_by(desc(model.id)))
            return result.unique().scalars().all()
        
    async def get_first_with_joinedload(
        self, 
        model: Type[SQLModel], 
        target: Union[dict, SQLModel], 
        keys: list[str], 
        with_soft_deleted: bool = False
    ) -> Optional[SQLModel]:
        async with self as db:
            query = self.build_select_query_with_joinedload(model, target, keys, with_soft_deleted)
            result = await db.session.execute(query.order_by(desc(model.id)).limit(1))
            return result.unique().scalars().first()
        
    async def get_one_or_none_with_joinedload(
        self, 
        model: Type[SQLModel], 
        target: Union[dict, SQLModel], 
        keys: list[str], 
        with_soft_deleted: bool = False
    ) -> Optional[SQLModel]:
        async with self as db:
            query = self.build_select_query_with_joinedload(model, target, keys, with_soft_deleted)
            result = await db.session.execute(query)
            return result.unique().scalars().one_or_none()
    
    async def create(self, instance: SQLModel):
        async with self as db:
            async with db.session.begin():
                db.session.add(instance)
            await db.session.refresh(instance)

    async def update_one(
        self, 
        model: Type[SQLModel], 
        filters: dict, 
        fields_to_update: dict
    ) -> Optional[SQLModel]:
        async with self as db:
            async with db.session.begin():
                query = self.build_select_query(model, filters, with_soft_deleted=False)
                result = await db.session.execute(query)
                record = result.scalars().one_or_none()

                if record:
                    for key, value in fields_to_update.items():
                        setattr(record, key, value)
                
                return record

    async def update_all(
        self, 
        model: Type[SQLModel], 
        filters: dict, 
        fields_to_update: dict
    ) -> list[SQLModel]:
        async with self as db:
            async with db.session.begin():
                query = self.build_select_query(model, filters, with_soft_deleted=False)
                result = await db.session.execute(query.order_by(desc(model.id)))
                records = result.scalars().all()

                for record in records:
                    for key, value in fields_to_update.items():
                        setattr(record, key, value)
                
                return records
    
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
  
    async def delete(
        self, 
        model: Type[SQLModel], 
        target: Union[dict, SQLModel], 
        soft_delete: bool
    ) -> None:
        async with self as db:
            async with db.session.begin():
                query = self.build_select_query(model, target, with_soft_deleted=True)
                result = await db.session.execute(query)
                existing_records = result.scalars().all()

                if existing_records:
                    if soft_delete:
                        current_time = datetime.utcnow()
                        for existing_record in existing_records:
                            setattr(existing_record, 'deleted_at', current_time)
                    else:
                        for existing_record in existing_records:
                            await db.session.delete(existing_record)

    async def bulk_delete(
        self, 
        model: Type[SQLModel], 
        target: Union[dict, SQLModel], 
        soft_delete: bool
    ) -> None:
        async with self as db:
            async with db.session.begin():
                query = self.build_select_query(model, target, with_soft_deleted=True)
                
                if soft_delete:
                    await db.session.execute(
                        update(model)
                        .where(query.whereclause)
                        .values(deleted_at=datetime.utcnow())
                    )
                else:
                    await db.session.execute(
                        delete(model)
                        .where(query.whereclause)
                    )