"""create bank accounts table

Revision ID: _2024_09_15_114551
Revises: _2024_09_15_114550
Create Date: 2024-09-15 11:45:52.437307

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '_2024_09_15_114551'
down_revision: Union[str, None] = '_2024_09_15_114550'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('bank_accounts',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('account', sa.String(length=255), nullable=False),
    sa.Column('issuer_id', sa.Integer(), sa.ForeignKey('bank_account_issuers.id', ondelete='CASCADE'), nullable=False),
    sa.Column('currency_id', sa.Integer(), sa.ForeignKey('currencies.id', ondelete='CASCADE'), nullable=False),
    sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_bank_accounts_currency_id'), 'bank_accounts', ['currency_id'], unique=False)
    op.create_index(op.f('ix_bank_accounts_user_id'), 'bank_accounts', ['user_id'], unique=False)


def downgrade() -> None:
    with op.batch_alter_table('bank_accounts') as batch_op:
        batch_op.drop_constraint('bank_accounts_ibfk_1', type_='foreignkey')

    with op.batch_alter_table('bank_accounts') as batch_op:
        batch_op.drop_constraint('bank_accounts_ibfk_2', type_='foreignkey')

    with op.batch_alter_table('bank_accounts') as batch_op:
        batch_op.drop_constraint('bank_accounts_ibfk_3', type_='foreignkey')
        
    op.drop_index(op.f('ix_bank_accounts_user_id'), table_name='bank_accounts')
    op.drop_index(op.f('ix_bank_accounts_currency_id'), table_name='bank_accounts')
    op.drop_table('bank_accounts')