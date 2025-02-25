"""add gender to profile

Revision ID: d898d03a6b90
Revises: 98d532615b77
Create Date: 2025-02-25 15:19:43.154945

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d898d03a6b90"
down_revision: Union[str, None] = "98d532615b77"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "profiles",
        sa.Column("gender", sa.Enum("male", "female", name="gender"), nullable=False),
    )


def downgrade() -> None:
    op.drop_column("profiles", "gender")
