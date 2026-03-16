"""convert_timestamps_to_timezone_aware

Revision ID: 930fe3cfb8f3
Revises: 002
Create Date: 2025-12-31 00:34:30.090354

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '930fe3cfb8f3'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Convert all timestamp columns to TIMESTAMP WITH TIME ZONE
    op.execute("ALTER TABLE tasks ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE USING created_at AT TIME ZONE 'UTC'")
    op.execute("ALTER TABLE tasks ALTER COLUMN updated_at TYPE TIMESTAMP WITH TIME ZONE USING updated_at AT TIME ZONE 'UTC'")
    op.execute("ALTER TABLE tasks ALTER COLUMN due_date TYPE TIMESTAMP WITH TIME ZONE USING due_date AT TIME ZONE 'UTC'")


def downgrade() -> None:
    # Convert back to TIMESTAMP WITHOUT TIME ZONE
    op.execute("ALTER TABLE tasks ALTER COLUMN created_at TYPE TIMESTAMP WITHOUT TIME ZONE")
    op.execute("ALTER TABLE tasks ALTER COLUMN updated_at TYPE TIMESTAMP WITHOUT TIME ZONE")
    op.execute("ALTER TABLE tasks ALTER COLUMN due_date TYPE TIMESTAMP WITHOUT TIME ZONE")
