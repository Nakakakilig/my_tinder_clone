"""add age to profile

Revision ID: 19c5db7c3c9c
Revises: d898d03a6b90
Create Date: 2025-02-28 16:18:44.466995

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "19c5db7c3c9c"
down_revision: Union[str, None] = "d898d03a6b90"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("profiles", sa.Column("age", sa.Integer(), nullable=False))


def downgrade() -> None:
    op.drop_column("profiles", "age")
