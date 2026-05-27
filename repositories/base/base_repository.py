from datetime import datetime
from sqlmodel import SQLModel
from db.base.base_db import BaseDB 
from sqlalchemy import desc, update, delete
from sqlalchemy.dialects.mysql import insert
from typing import Type, Union, Optional, Any

class BaseRepository:
    def __init__(self, model: Type[SQLModel]):
        self.model = model
        
    async def get_all(
        self, 
        target: Optional[Union[dict, SQLModel]] = None,
        with_soft_deleted: bool = False
    ) -> list[Any]:
        async with BaseDB() as db:
            query = db.build_select_query(self.model, target or {}, with_soft_deleted)
            result = await db.session.execute(query.order_by(desc(self.model.id)))
            
            return result.scalars().all()
        
    async def get_first(
        self, 
        target: Union[dict, SQLModel],
        with_soft_deleted: bool = False
    ) -> Optional[Any]:
        async with BaseDB() as db:
            query = db.build_select_query(self.model, target, with_soft_deleted)
            result = await db.session.execute(query.order_by(desc(self.model.id)).limit(1))

            return result.scalars().first()
        
    async def get_one_or_none(
        self, 
        target: Union[dict, SQLModel], 
        with_soft_deleted: bool = False
    ) -> Optional[Any]:
        async with BaseDB() as db:
            query = db.build_select_query(self.model, target, with_soft_deleted)
            result = await db.session.execute(query)

            return result.scalars().one_or_none()

    async def get_all_with_joinedload(
        self, 
        target: Optional[Union[dict, SQLModel]] = None,
        keys: list[str] = None, 
        with_soft_deleted: bool = False
    ) -> list[Any]:
        async with BaseDB() as db:
            query = db.build_select_query_with_joinedload(self.model, target or {}, keys, with_soft_deleted)
            result = await db.session.execute(query.order_by(desc(self.model.id)))
            res = result.unique().scalars().all()
            
            if not with_soft_deleted:
                return self.model.clean_soft_deleted_relations(res)
            
            return res
        
    async def get_first_with_joinedload(
        self, 
        target: Union[dict, SQLModel], 
        keys: list[str], 
        with_soft_deleted: bool = False
    ) -> Optional[Any]:
        async with BaseDB() as db:
            query = db.build_select_query_with_joinedload(self.model, target, keys, with_soft_deleted)
            result = await db.session.execute(query.order_by(desc(self.model.id)).limit(1))
            res = result.unique().scalars().first()
            
            if res and not with_soft_deleted:
                return self.model.clean_soft_deleted_relations(res)
            
            return res
        
    async def get_one_or_none_with_joinedload(
        self, 
        target: Union[dict, SQLModel], 
        keys: list[str], 
        with_soft_deleted: bool = False
    ) -> Optional[Any]:
        async with BaseDB() as db:
            query = db.build_select_query_with_joinedload(self.model, target, keys, with_soft_deleted)
            result = await db.session.execute(query)
            res = result.unique().scalars().one_or_none()
            
            if res and not with_soft_deleted:
                return self.model.clean_soft_deleted_relations(res)
            
            return res
    
    async def create(self, instance: SQLModel) -> None:
        async with BaseDB() as db:
            async with db.session.begin():
                db.session.add(instance)
            await db.session.refresh(instance)

    async def update_one(
        self, 
        target: dict, 
        fields_to_update: dict
    ) -> Optional[Any]:
        async with BaseDB() as db:
            async with db.session.begin():
                query = db.build_select_query(self.model, target, with_soft_deleted=False)
                result = await db.session.execute(query)
                record = result.scalars().one_or_none()

                if record:
                    for key, value in fields_to_update.items():
                        setattr(record, key, value)

                return record

    async def update_all(
        self, 
        target: dict, 
        fields_to_update: dict
    ) -> list[Any]:
        async with BaseDB() as db:
            async with db.session.begin():
                query = db.build_select_query(self.model, target, with_soft_deleted=False)
                result = await db.session.execute(query.order_by(desc(self.model.id)))
                records = result.scalars().all()

                for record in records:
                    for key, value in fields_to_update.items():
                        setattr(record, key, value)

                return records
    
    async def create_or_update(self, instance: SQLModel) -> None:
        async with BaseDB() as db:
            instance_properties = dict(instance)
            instance_properties['updated_at'] = datetime.utcnow()

            async with db.session.begin():
                await db.session.execute(
                    insert(self.model)
                    .values(**instance_properties)
                    .on_duplicate_key_update(**instance_properties)
                )

    async def seed(self, instances: list[SQLModel]) -> None:
        for index, instance in enumerate(instances):
            instance.id = index + 1
            await self.create_or_update(instance)
  
    async def delete(
        self,
        soft_delete: bool,
        target: Optional[Union[dict, SQLModel]] = None,
    ) -> None:
        async with BaseDB() as db:
            async with db.session.begin():
                query = db.build_select_query(self.model, target or {}, with_soft_deleted=True)
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
        soft_delete: bool,
        target: Optional[Union[dict, SQLModel]] = None,
    ) -> None:
        async with BaseDB() as db:
            async with db.session.begin():
                query = db.build_select_query(self.model, target or {}, with_soft_deleted=True)
                
                if soft_delete:
                    await db.session.execute(
                        update(self.model)
                        .where(query.whereclause)
                        .values(deleted_at=datetime.utcnow())
                    )
                else:
                    await db.session.execute(
                        delete(self.model)
                        .where(query.whereclause)
                    )