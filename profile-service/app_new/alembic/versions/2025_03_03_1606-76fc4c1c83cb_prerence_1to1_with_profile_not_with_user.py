"""prerence 1to1 with profile, not with user

Revision ID: 76fc4c1c83cb
Revises: 19c5db7c3c9c
Create Date: 2025-03-03 16:06:29.556197

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "76fc4c1c83cb"
down_revision: Union[str, None] = "19c5db7c3c9c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("preferences", sa.Column("profile_id", sa.Integer(), nullable=False))
    op.drop_index("ix_preferences_user_id", table_name="preferences")
    op.create_index(
        op.f("ix_preferences_profile_id"),
        "preferences",
        ["profile_id"],
        unique=True,
    )
    op.drop_constraint(
        "fk_preferences_user_id_users", "preferences", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("fk_preferences_profile_id_profiles"),
        "preferences",
        "profiles",
        ["profile_id"],
        ["id"],
    )
    op.drop_column("preferences", "user_id")


def downgrade() -> None:
    op.add_column(
        "preferences",
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(
        op.f("fk_preferences_profile_id_profiles"),
        "preferences",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_preferences_user_id_users",
        "preferences",
        "users",
        ["user_id"],
        ["id"],
    )
    op.drop_index(op.f("ix_preferences_profile_id"), table_name="preferences")
    op.create_index("ix_preferences_user_id", "preferences", ["user_id"], unique=True)
    op.drop_column("preferences", "profile_id")
