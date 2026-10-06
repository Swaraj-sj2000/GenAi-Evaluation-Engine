"""add run user ownership

Revision ID: 9f2b4c1a7d8e
Revises: 32b7adb42c9e
Create Date: 2026-10-06 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9f2b4c1a7d8e"
down_revision: Union[str, Sequence[str], None] = "32b7adb42c9e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("runs") as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.Integer(), nullable=True))
        batch_op.create_index(batch_op.f("ix_runs_user_id"), ["user_id"], unique=False)
        batch_op.create_foreign_key("fk_runs_user_id_users", "users", ["user_id"], ["id"])


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("runs") as batch_op:
        batch_op.drop_constraint("fk_runs_user_id_users", type_="foreignkey")
        batch_op.drop_index(batch_op.f("ix_runs_user_id"))
        batch_op.drop_column("user_id")
