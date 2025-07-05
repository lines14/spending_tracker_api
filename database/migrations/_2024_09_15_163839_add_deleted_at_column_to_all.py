"""add deleted at column to all

Revision ID: _2024_09_15_163839
Revises: _2024_09_15_115304
Create Date: 2024-09-15 16:38:40.371171

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '_2024_09_15_163839'
down_revision: Union[str, None] = '_2024_09_15_115304'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("purchases") as batch_op:
        batch_op.add_column(
            sa.Column('deleted_at', sa.DateTime(), nullable=True)
        )

    with op.batch_alter_table("sessions") as batch_op:
        batch_op.add_column(
            sa.Column('deleted_at', sa.DateTime(), nullable=True)
        )

    with op.batch_alter_table("bank_account_issuers") as batch_op:
        batch_op.add_column(
            sa.Column('deleted_at', sa.DateTime(), nullable=True)
        )

    with op.batch_alter_table("bank_accounts") as batch_op:
        batch_op.add_column(
            sa.Column('deleted_at', sa.DateTime(), nullable=True)
        )

    with op.batch_alter_table("migrations") as batch_op:
        batch_op.add_column(
            sa.Column('deleted_at', sa.DateTime(), nullable=True)
        )

    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(
            sa.Column('deleted_at', sa.DateTime(), nullable=True)
        )

    with op.batch_alter_table("product_groups") as batch_op:
        batch_op.add_column(
            sa.Column('deleted_at', sa.DateTime(), nullable=True)
        )

    with op.batch_alter_table("product_types") as batch_op:
        batch_op.add_column(
            sa.Column('deleted_at', sa.DateTime(), nullable=True)
        )

    with op.batch_alter_table("product_sub_types") as batch_op:
        batch_op.add_column(
            sa.Column('deleted_at', sa.DateTime(), nullable=True)
        )

    with op.batch_alter_table("currencies") as batch_op:
        batch_op.add_column(
            sa.Column('deleted_at', sa.DateTime(), nullable=True)
        )
        
    with op.batch_alter_table("currency_rates") as batch_op:
        batch_op.add_column(
            sa.Column('deleted_at', sa.DateTime(), nullable=True)
        )


def downgrade() -> None:
    op.drop_column('currency_rates', 'deleted_at')
    op.drop_column('currencies', 'deleted_at')
    op.drop_column('product_sub_types', 'deleted_at')
    op.drop_column('product_types', 'deleted_at')
    op.drop_column('product_groups', 'deleted_at')
    op.drop_column('users', 'deleted_at')
    op.drop_column('migrations', 'deleted_at')
    op.drop_column('bank_accounts', 'deleted_at')
    op.drop_column('bank_account_issuers', 'deleted_at')
    op.drop_column('sessions', 'deleted_at')
    op.drop_column('purchases', 'deleted_at')