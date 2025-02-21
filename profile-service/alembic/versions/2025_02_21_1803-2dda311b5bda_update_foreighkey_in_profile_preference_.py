"""update foreighkey in profile, preference and photos

Revision ID: 2dda311b5bda
Revises: 832cc334bd7e
Create Date: 2025-02-21 18:03:10.030659

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2dda311b5bda"
down_revision: Union[str, None] = "832cc334bd7e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("fk_photos_user_id_profiles", "photos", type_="foreignkey")
    op.create_foreign_key(
        op.f("fk_photos_user_id_users"), "photos", "users", ["user_id"], ["id"]
    )
    op.drop_constraint(
        "fk_preferences_user_id_profiles", "preferences", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("fk_preferences_user_id_users"),
        "preferences",
        "users",
        ["user_id"],
        ["id"],
    )
    op.add_column("profiles", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_index(op.f("ix_profiles_user_id"), "profiles", ["user_id"], unique=True)
    op.create_foreign_key(
        op.f("fk_profiles_user_id_users"),
        "profiles",
        "users",
        ["user_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("fk_profiles_user_id_users"), "profiles", type_="foreignkey"
    )
    op.drop_index(op.f("ix_profiles_user_id"), table_name="profiles")
    op.drop_column("profiles", "user_id")
    op.drop_constraint(
        op.f("fk_preferences_user_id_users"), "preferences", type_="foreignkey"
    )
    op.create_foreign_key(
        "fk_preferences_user_id_profiles",
        "preferences",
        "profiles",
        ["user_id"],
        ["id"],
    )
    op.drop_constraint(op.f("fk_photos_user_id_users"), "photos", type_="foreignkey")
    op.create_foreign_key(
        "fk_photos_user_id_profiles", "photos", "profiles", ["user_id"], ["id"]
    )
