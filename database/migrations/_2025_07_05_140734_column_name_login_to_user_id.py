"""column name login to user id

Revision ID: _2025_07_05_140734
Revises: _2025_07_05_115234
Create Date: 2025-07-05 14:07:35.468052

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '_2025_07_05_140734'
down_revision: Union[str, None] = '_2025_07_05_115234'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index(op.f('ix_sessions_login'), table_name='sessions')
    op.alter_column(
        'sessions', 
        'login', 
        new_column_name='user_id',
        existing_type=sa.String(length=255),
        type_=sa.Integer(),
        existing_nullable=False
    )
    op.create_index(op.f('ix_sessions_user_id'), 'sessions', ['user_id'], unique=False)
    op.create_foreign_key(
        constraint_name='sessions_ibfk_1',
        source_table='sessions',
        referent_table='users',
        local_cols=['user_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    with op.batch_alter_table('sessions') as batch_op:
        batch_op.drop_constraint('sessions_ibfk_1', type_='foreignkey')
    op.drop_index(op.f('ix_sessions_user_id'), table_name='sessions')
    op.alter_column(
        'sessions', 
        'user_id', 
        new_column_name='login',
        existing_type=sa.Integer(),
        type_=sa.String(length=255),
        existing_nullable=False
    )
    op.create_index(op.f('ix_sessions_login'), 'sessions', ['login'], unique=False)