"""create error logs table

Revision ID: _2025_07_05_115234
Revises: _2024_09_15_163839
Create Date: 2025-07-05 11:52:35.446474

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '_2025_07_05_115234'
down_revision: Union[str, None] = '_2024_09_15_163839'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('error_logs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('file', sa.String(length=255), nullable=True),
    sa.Column('line', sa.Integer(), nullable=True),
    sa.Column('snippet', sa.String(length=255), nullable=True),
    sa.Column('stack', sa.Text(), nullable=True),
    sa.Column('message', sa.String(length=255), nullable=False),
    sa.Column('code', sa.Integer(), nullable=True),
    sa.Column('body', sa.String(length=255), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_error_logs_message'), 'error_logs', ['message'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_error_logs_message'), table_name='error_logs')
    op.drop_table('error_logs')
