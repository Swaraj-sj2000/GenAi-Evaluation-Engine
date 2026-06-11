"""add reasoning to runs

Revision ID: 32b7adb42c9e
Revises: c7d5acd758db
Create Date: 2026-06-11 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32b7adb42c9e'
down_revision: Union[str, Sequence[str], None] = 'c7d5acd758db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('runs', sa.Column('reasoning', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('runs', 'reasoning')
