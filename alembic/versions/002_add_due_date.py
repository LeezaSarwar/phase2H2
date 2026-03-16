"""Add due_date to tasks

Revision ID: 002
Revises: 001
Create Date: 2025-12-30

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add due_date column to tasks table
    op.add_column("tasks", sa.Column("due_date", sa.DateTime(), nullable=True))
    op.create_index("idx_tasks_due_date", "tasks", ["due_date"])


def downgrade() -> None:
    op.drop_index("idx_tasks_due_date")
    op.drop_column("tasks", "due_date")
