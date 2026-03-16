"""add_category_and_priority_to_tasks

Revision ID: 9f6aa00b8851
Revises: 930fe3cfb8f3
Create Date: 2025-12-31 00:55:51.235205

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '9f6aa00b8851'
down_revision: Union[str, None] = '930fe3cfb8f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add category column with default 'Personal'
    op.add_column('tasks', sa.Column('category', sa.String(length=50), nullable=False, server_default='Personal'))
    # Add priority column with default 'Medium'
    op.add_column('tasks', sa.Column('priority', sa.String(length=20), nullable=False, server_default='Medium'))

    # Create indexes for better query performance
    op.create_index('idx_tasks_category', 'tasks', ['category'])
    op.create_index('idx_tasks_priority', 'tasks', ['priority'])


def downgrade() -> None:
    op.drop_index('idx_tasks_priority')
    op.drop_index('idx_tasks_category')
    op.drop_column('tasks', 'priority')
    op.drop_column('tasks', 'category')
