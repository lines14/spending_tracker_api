from sqlalchemy import func
from datetime import datetime, timezone
from sqlmodel import TIMESTAMP, Field, SQLModel

class WithTimestamps(SQLModel):
    created_at: datetime = Field(
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={"server_default": func.now()},
        nullable=False,
    )

    updated_at: datetime = Field(
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={
            "onupdate": lambda: datetime.now(timezone.utc),
            "server_default": func.now(),
        },
        nullable=False,
    )