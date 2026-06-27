"""remove deleted at column from sessions

Revision ID: _2026_06_27_105712
Revises: _2025_07_05_203154
Create Date: 2026-06-27 10:57:12.501594

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '_2026_06_27_105712'
down_revision: Union[str, None] = '_2025_07_05_203154'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('sessions', 'deleted_at')


def downgrade() -> None:
    with op.batch_alter_table("sessions") as batch_op:
        batch_op.add_column(
            sa.Column('deleted_at', sa.DateTime(), nullable=True)
        )
