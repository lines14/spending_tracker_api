from sqlmodel import Field
from typing import Optional
from datetime import datetime
from database.base.database import Database
from models.base.base_model import BaseModel
from sqlalchemy import func, Column, DateTime

class User(BaseModel, table=True):
    __tablename__ = 'users'
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    created_at: datetime = Field(sa_column=Column(DateTime, server_default=func.now(), nullable=False))
    updated_at: datetime = Field(sa_column=Column(DateTime, server_default=func.now(), nullable=False, onupdate=func.now))
    login: str = Field(index=True, nullable=False)
    password: str = Field(nullable=False)

    async def create(self):
        async with Database() as database:
            await database.create(self)

    async def get(self):
        async with Database() as database:
            return await database.get(self)