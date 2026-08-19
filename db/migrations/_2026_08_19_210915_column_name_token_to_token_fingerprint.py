"""column name token to token fingerprint

Revision ID: _2026_08_19_210915
Revises: _2026_06_28_164356
Create Date: 2026-08-19 21:09:16.226388

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '_2026_08_19_210915'
down_revision: Union[str, None] = '_2026_06_28_164356'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        'sessions', 
        'token', 
        new_column_name='token_fingerprint',
        existing_type=sa.String(length=255),
        existing_nullable=False
    )


def downgrade():
    op.alter_column(
        'sessions', 
        'token_fingerprint', 
        new_column_name='token',
        existing_type=sa.String(length=255),
        existing_nullable=False
    )