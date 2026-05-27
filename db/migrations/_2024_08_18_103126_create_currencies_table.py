"""create currencies table

Revision ID: _2024_08_18_103126
Revises: _2024_08_18_092749
Create Date: 2024-08-18 10:31:27.942603

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '_2024_08_18_103126'
down_revision: Union[str, None] = '_2024_08_18_092749'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('currencies',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('currency', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('currencies')