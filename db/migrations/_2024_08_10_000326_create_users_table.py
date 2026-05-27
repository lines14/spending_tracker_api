"""create users table

Revision ID: _2024_08_10_000326
Revises: _2024_08_10_000100
Create Date: 2024-08-10 00:03:26.917411

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '_2024_08_10_000326'
down_revision: Union[str, None] = '_2024_08_10_000100'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('login', sa.String(length=255), nullable=False),
    sa.Column('token', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    
    op.create_index(op.f('ix_users_login'), 'users', ['login'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_users_login'), table_name='users')
    op.drop_table('users')