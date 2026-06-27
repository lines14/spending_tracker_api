from typing import Optional
from datetime import datetime
from sqlmodel import TIMESTAMP, Field, SQLModel

class WithSoftDelete(SQLModel):
    deleted_at: Optional[datetime] = Field(
        sa_type=TIMESTAMP(timezone=True),
        nullable=True,
    )