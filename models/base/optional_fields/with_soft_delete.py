from datetime import datetime

from sqlmodel import TIMESTAMP, Field, SQLModel


class WithSoftDelete(SQLModel):
    deleted_at: datetime | None = Field(
        sa_type=TIMESTAMP(timezone=True),
        nullable=True,
    )
