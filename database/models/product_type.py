from sqlalchemy.sql import func
from database.base.database import Database
from sqlalchemy import Column, Integer, String, DateTime

class ProductType(Database):
    __tablename__ = 'product_types'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    type = Column(String(255), nullable=False)
    group_id = Column(Integer, index=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __init__(self, type=None, group_id=None):
        self.db = Database()
        self.type = type
        self.group_id = group_id

    def get(self):
        return self.db.get(self)