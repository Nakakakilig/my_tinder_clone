"""create db

Revision ID: 19ff2915d9c0
Revises:
Create Date: 2025-03-19 15:00:38.935108

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "19ff2915d9c0"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("username", name=op.f("uq_users_username")),
    )
    op.create_table(
        "profiles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=20), nullable=False),
        sa.Column("last_name", sa.String(length=20), nullable=False),
        sa.Column("gender", sa.Enum("male", "female", name="gender"), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("geo_latitude", sa.Float(), nullable=False),
        sa.Column("geo_longitude", sa.Float(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_profiles_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_profiles")),
    )
    op.create_index(op.f("ix_profiles_user_id"), "profiles", ["user_id"], unique=True)
    op.create_table(
        "photos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("profile_id", sa.Integer(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["profile_id"],
            ["profiles.id"],
            name=op.f("fk_photos_profile_id_profiles"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_photos")),
    )
    op.create_table(
        "preferences",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("profile_id", sa.Integer(), nullable=False),
        sa.Column("gender", sa.Enum("male", "female", name="gender"), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("radius", sa.Integer(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["profile_id"],
            ["profiles.id"],
            name=op.f("fk_preferences_profile_id_profiles"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_preferences")),
    )
    op.create_index(
        op.f("ix_preferences_profile_id"),
        "preferences",
        ["profile_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_preferences_profile_id"), table_name="preferences")
    op.drop_table("preferences")
    op.drop_table("photos")
    op.drop_index(op.f("ix_profiles_user_id"), table_name="profiles")
    op.drop_table("profiles")
    op.drop_table("users")
