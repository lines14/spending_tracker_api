"""create product groups table

Revision ID: _2024_08_17_124155
Revises: _2024_08_10_002012
Create Date: 2024-08-17 12:41:57.026620

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '_2024_08_17_124155'
down_revision: Union[str, None] = '_2024_08_10_002012'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('product_groups',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('group', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('product_groups')