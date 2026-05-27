"""add host column to users

Revision ID: _2024_08_10_001938
Revises: _2024_08_10_000326
Create Date: 2024-08-10 00:19:39.034658

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '_2024_08_10_001938'
down_revision: Union[str, None] = '_2024_08_10_000326'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("users", recreate='always') as batch_op:
        batch_op.add_column(
            sa.Column('host', sa.String(length=255), nullable=False),
            insert_after="login"
        )


def downgrade() -> None:
    op.drop_column('users', 'host')