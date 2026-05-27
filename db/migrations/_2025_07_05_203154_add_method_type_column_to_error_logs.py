"""add method type column to error logs

Revision ID: _2025_07_05_203154
Revises: _2025_07_05_140734
Create Date: 2025-07-05 20:31:55.052888

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '_2025_07_05_203154'
down_revision: Union[str, None] = '_2025_07_05_140734'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("error_logs", recreate='always') as batch_op:
        batch_op.add_column(
            sa.Column('method_type', sa.String(length=255), nullable=True),
            insert_after="code"
        )


def downgrade() -> None:
    op.drop_column('error_logs', 'method_type')
