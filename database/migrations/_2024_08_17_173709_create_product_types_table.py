"""create product types table

Revision ID: _2024_08_17_173709
Revises: _2024_08_17_124155
Create Date: 2024-08-17 17:37:10.306231

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '_2024_08_17_173709'
down_revision: Union[str, None] = '_2024_08_17_124155'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('product_types',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('type', sa.String(length=255), nullable=False),
    sa.Column('group_id', sa.Integer(), sa.ForeignKey('product_groups.id', ondelete='CASCADE'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_product_types_group_id'), 'product_types', ['group_id'], unique=False)


def downgrade() -> None:
    with op.batch_alter_table('product_types') as batch_op:
        batch_op.drop_constraint('product_types_ibfk_1', type_='foreignkey')
        
    op.drop_index(op.f('ix_product_types_group_id'), table_name='product_types')
    op.drop_table('product_types')