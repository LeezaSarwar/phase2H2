"""Initial schema

Revision ID: 001
Revises:
Create Date: 2025-12-29

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("idx_users_email", "users", ["email"], unique=True)

    # Create tasks table
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("completed", sa.Boolean(), default=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )

    # Create indexes for tasks
    op.create_index("idx_tasks_user_id", "tasks", ["user_id"])
    op.create_index("idx_tasks_completed", "tasks", ["completed"])
    op.create_index("idx_tasks_created_at", "tasks", ["created_at"])


def downgrade() -> None:
    op.drop_index("idx_tasks_created_at")
    op.drop_index("idx_tasks_completed")
    op.drop_index("idx_tasks_user_id")
    op.drop_table("tasks")
    op.drop_index("idx_users_email")
    op.drop_table("users")
