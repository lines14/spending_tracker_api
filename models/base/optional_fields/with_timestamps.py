from datetime import UTC, datetime

from sqlalchemy import func
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
            "onupdate": lambda: datetime.now(UTC),
            "server_default": func.now(),
        },
        nullable=False,
    )
