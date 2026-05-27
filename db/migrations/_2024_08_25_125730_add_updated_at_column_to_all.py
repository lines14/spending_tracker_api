"""add updated at column to all

Revision ID: _2024_08_25_125730
Revises: _2024_08_24_200038
Create Date: 2024-08-25 12:57:32.163727

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '_2024_08_25_125730'
down_revision: Union[str, None] = '_2024_08_24_200038'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("migrations") as batch_op:
        batch_op.add_column(
            sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False)
        )

    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(
            sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False)
        )

    with op.batch_alter_table("product_groups") as batch_op:
        batch_op.add_column(
            sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False)
        )

    with op.batch_alter_table("product_types") as batch_op:
        batch_op.add_column(
            sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False)
        )

    with op.batch_alter_table("product_sub_types") as batch_op:
        batch_op.add_column(
            sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False)
        )

    with op.batch_alter_table("currencies") as batch_op:
        batch_op.add_column(
            sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False)
        )
        
    with op.batch_alter_table("currency_rates") as batch_op:
        batch_op.add_column(
            sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False)
        )


def downgrade() -> None:
    op.drop_column('currency_rates', 'updated_at')
    op.drop_column('currencies', 'updated_at')
    op.drop_column('product_sub_types', 'updated_at')
    op.drop_column('product_types', 'updated_at')
    op.drop_column('product_groups', 'updated_at')
    op.drop_column('users', 'updated_at')
    op.drop_column('migrations', 'updated_at')