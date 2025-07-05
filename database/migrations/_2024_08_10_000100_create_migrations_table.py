"""create migrations table

Revision ID: _2024_08_10_000100
Revises: 
Create Date: 2024-08-10 00:01:01.356578

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '_2024_08_10_000100'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('migrations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('version', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('version')
    )
    
    op.create_index(op.f('ix_migrations_version'), 'migrations', ['version'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_migrations_version'), table_name='migrations')
    op.drop_table('migrations')