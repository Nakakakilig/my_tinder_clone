"""remove username in profile

Revision ID: dc3407f2247d
Revises: da6d63b61a64
Create Date: 2025-02-21 17:43:59.775519

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dc3407f2247d"
down_revision: Union[str, None] = "da6d63b61a64"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index("ix_preferences_user_id", table_name="preferences")
    op.create_index(
        op.f("ix_preferences_user_id"), "preferences", ["user_id"], unique=True
    )
    op.drop_constraint("uq_profiles_username", "profiles", type_="unique")
    op.drop_column("profiles", "username")


def downgrade() -> None:
    op.add_column(
        "profiles",
        sa.Column(
            "username",
            sa.VARCHAR(length=15),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.create_unique_constraint("uq_profiles_username", "profiles", ["username"])
    op.drop_index(op.f("ix_preferences_user_id"), table_name="preferences")
    op.create_index("ix_preferences_user_id", "preferences", ["user_id"], unique=False)
