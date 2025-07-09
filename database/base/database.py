from config import Config
from datetime import datetime
from sqlalchemy import inspect, desc, select
from sqlalchemy.orm import DeclarativeBase, joinedload
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

class Database(DeclarativeBase):
    def __init__(self): # if sqlite add arg: connect_args={'check_same_thread': False}
        self.engine = create_async_engine(Config().DB_URL_ASYNC)

        self.sessionmaker = async_sessionmaker(
            bind=self.engine, 
            expire_on_commit=False, 
            autocommit=False, 
            autoflush=False
        )

    async def init_tables(self):
        async with self.engine.begin() as connection:
            await connection.run_sync(self.metadata.create_all)

    async def __aenter__(self):
        self.session = self.sessionmaker()
        await self.init_tables()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, 'session'):
            await self.session.close()

        await self.engine.dispose()

    @staticmethod
    def build_nested_joinedload(model, key: str):
        parts = key.split(".")
        loader = joinedload(getattr(model, parts[0]))
        current_model = model.__mapper__.relationships[parts[0]].mapper.class_

        for part in parts[1:]:
            loader = loader.joinedload(getattr(current_model, part))
            current_model = current_model.__mapper__.relationships[part].mapper.class_

        return loader

    async def get_not_empty_properties(self, instance):
        instance_properties = {attr.key: getattr(instance, attr.key) for attr in inspect(instance).mapper.column_attrs}

        return {key: value for key, value in instance_properties.items() if value is not None}

    async def create_or_update(self, instance):
        instance_properties = await self.get_not_empty_properties(instance)
        properties_for_update = instance_properties

        if 'id' in instance_properties:
            instance_properties = {key: value for key, value in instance_properties.items() if key == 'id'}

        filter_expressions = [getattr(type(instance), key) == value for key, value in instance_properties.items()]

        async with self.session.begin():
            existing_record = (await self.session.execute(
                select(type(instance)).filter(*filter_expressions).order_by(desc(type(instance).id))
            )).scalars().first()

            if existing_record:
                for attr, value in properties_for_update.items():
                    setattr(existing_record, attr, value)
                    setattr(existing_record, 'updated_at', datetime.utcnow())
            else:
                self.session.add(instance)

            await self.session.commit()

    async def seed(self, instances):
        async with self as db:
            for index, instance in enumerate(instances):
                instance.id = index + 1
                await db.create_or_update(instance)
                
    async def delete(self, instance, soft_delete: bool):
        async with self as db:
            instance_properties = await self.get_not_empty_properties(instance)

            if 'id' in instance_properties:
                instance_properties = {key: value for key, value in instance_properties.items() if key == 'id'}

            filter_expressions = [getattr(type(instance), key) == value for key, value in instance_properties.items()]

            async with db.session.begin():
                existing_record = (await db.session.execute(
                    select(type(instance)).filter(*filter_expressions).order_by(desc(type(instance).id))
                )).scalars().first()

                if existing_record:
                    if soft_delete:
                        setattr(existing_record, 'deleted_at', datetime.utcnow())
                    else:
                        await db.session.delete(existing_record)

                await db.session.commit()

    async def create(self, instance):
        async with self as db:
            async with db.session.begin():
                db.session.add(instance)
                await db.session.commit()

            await db.session.refresh(instance)

    async def get(self, instance, with_soft_deleted: bool):
        async with self as db:
            instance_properties = await self.get_not_empty_properties(instance)
            filter_expressions = [getattr(type(instance), key) == value for key, value in instance_properties.items()]

            if not with_soft_deleted:
                filter_expressions.append(getattr(type(instance), 'deleted_at') == None)

            async with db.session.begin():
                return (await db.session.execute(
                    select(type(instance)).filter(*filter_expressions).order_by(desc(type(instance).id))
                )).scalars().first()
    
    async def get_all(self, instance, with_soft_deleted: bool):
        async with self as db:
            query = select(type(instance))

            if not with_soft_deleted:
                query = query.filter(getattr(type(instance), 'deleted_at') == None)
                
            async with db.session.begin():
                return (await db.session.execute(query)).scalars().all()
            
    async def delete_all(self, instance, with_soft_deleted: bool, soft_delete: bool):
        async with self as db:
            query = select(type(instance))

            if not with_soft_deleted:
                query = query.filter(getattr(type(instance), 'deleted_at') == None)

            async with db.session.begin():
                existing_records = (await db.session.execute(query)).scalars().all()

                if len(existing_records) > 0:
                    if soft_delete:
                        for existing_record in existing_records:
                            setattr(existing_record, 'deleted_at', datetime.utcnow())
                    else:
                        for existing_record in existing_records:
                            await db.session.delete(existing_record)

                await db.session.commit()

    async def joined_load(self, instance, keys: list[str], with_soft_deleted: bool):
        async with self as db:
            options = [self.build_nested_joinedload(type(instance), key) for key in keys]
            query = select(type(instance)).options(*options)

            if not with_soft_deleted:
                query = query.filter(getattr(type(instance), "deleted_at") == None)

            async with db.session.begin():
                return (await db.session.execute(query)).unique().scalars().all()