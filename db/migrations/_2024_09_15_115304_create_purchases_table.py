"""create purchases table

Revision ID: _2024_09_15_115304
Revises: _2024_09_15_114551
Create Date: 2024-09-15 11:53:05.514238

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '_2024_09_15_115304'
down_revision: Union[str, None] = '_2024_09_15_114551'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('purchases',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cost', sa.Float(), nullable=False),
    sa.Column('account_id', sa.Integer(), sa.ForeignKey('bank_accounts.id', ondelete='CASCADE'), nullable=False),
    sa.Column('sub_type_id', sa.Integer(), sa.ForeignKey('product_sub_types.id', ondelete='CASCADE'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_purchases_account_id'), 'purchases', ['account_id'], unique=False)
    op.create_index(op.f('ix_purchases_sub_type_id'), 'purchases', ['sub_type_id'], unique=False)


def downgrade() -> None:
    with op.batch_alter_table('purchases') as batch_op:
        batch_op.drop_constraint('purchases_ibfk_1', type_='foreignkey')

    with op.batch_alter_table('purchases') as batch_op:
        batch_op.drop_constraint('purchases_ibfk_2', type_='foreignkey')
        
    op.drop_index(op.f('ix_purchases_sub_type_id'), table_name='purchases')
    op.drop_index(op.f('ix_purchases_account_id'), table_name='purchases')
    op.drop_table('purchases')