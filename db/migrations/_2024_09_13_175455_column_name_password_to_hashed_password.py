"""column name password to hashed password

Revision ID: _2024_09_13_175455
Revises: _2024_08_28_170941
Create Date: 2024-09-13 17:54:56.717875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '_2024_09_13_175455'
down_revision: Union[str, None] = '_2024_08_28_170941'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        'users', 
        'password', 
        new_column_name='hashed_password',
        existing_type=sa.String(length=255),
        existing_nullable=False
    )


def downgrade():
    op.alter_column(
        'users', 
        'hashed_password', 
        new_column_name='password',
        existing_type=sa.String(length=255),
        existing_nullable=False
    )