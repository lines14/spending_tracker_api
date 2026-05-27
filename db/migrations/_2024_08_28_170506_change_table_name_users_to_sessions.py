"""change table name users to sessions

Revision ID: _2024_08_28_170506
Revises: _2024_08_25_125730
Create Date: 2024-08-28 17:05:07.017948

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '_2024_08_28_170506'
down_revision: Union[str, None] = '_2024_08_25_125730'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_index(op.f('ix_users_login'), table_name='users')
    op.rename_table('users', 'sessions')
    op.create_index(op.f('ix_sessions_login'), 'sessions', ['login'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_sessions_login'), table_name='sessions')
    op.rename_table('sessions', 'users')
    op.create_index(op.f('ix_users_login'), 'users', ['login'], unique=False)