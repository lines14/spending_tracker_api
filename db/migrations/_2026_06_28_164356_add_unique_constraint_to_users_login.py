"""add unique constraint to users login

Revision ID: _2026_06_28_164356
Revises: _2026_06_27_105712
Create Date: 2026-06-28 16:43:57.086636

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '_2026_06_28_164356'
down_revision: Union[str, None] = '_2026_06_27_105712'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index('ix_users_login', table_name='users')
    op.create_index('ix_users_login', 'users', ['login'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_users_login', table_name='users')
    op.create_index('ix_users_login', 'users', ['login'], unique=False)
