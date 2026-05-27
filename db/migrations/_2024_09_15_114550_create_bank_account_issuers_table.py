"""create bank account issuers table

Revision ID: _2024_09_15_114550
Revises: _2024_09_13_175455
Create Date: 2024-09-15 11:45:51.437307

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '_2024_09_15_114550'
down_revision: Union[str, None] = '_2024_09_13_175455'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('bank_account_issuers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('issuer', sa.String(length=255), nullable=False),
    sa.Column('country_code', sa.String(length=3), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('bank_account_issuers')