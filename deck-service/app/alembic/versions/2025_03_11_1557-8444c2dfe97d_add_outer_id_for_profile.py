"""add outer_id for profile

Revision ID: 8444c2dfe97d
Revises: a61c7697be68
Create Date: 2025-03-11 15:57:18.626929

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8444c2dfe97d"
down_revision: Union[str, None] = "a61c7697be68"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("profiles", sa.Column("outer_id", sa.Integer(), nullable=False))


def downgrade() -> None:
    op.drop_column("profiles", "outer_id")
