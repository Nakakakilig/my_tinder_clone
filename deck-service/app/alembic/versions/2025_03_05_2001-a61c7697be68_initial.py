"""initial

Revision ID: a61c7697be68
Revises:
Create Date: 2025-03-05 20:01:05.877033

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a61c7697be68"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "profiles",
        sa.Column("id", sa.Integer(), nullable=False),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_profiles")),
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
    op.drop_table("profiles")
