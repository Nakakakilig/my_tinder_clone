"""create photo

Revision ID: da6d63b61a64
Revises: 4681d44e8f2a
Create Date: 2025-02-21 14:06:33.065144

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "da6d63b61a64"
down_revision: Union[str, None] = "4681d44e8f2a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "photos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("url", sa.String(length=100), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["profiles.id"],
            name=op.f("fk_photos_user_id_profiles"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_photos")),
    )
    op.create_index(op.f("ix_photos_user_id"), "photos", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_photos_user_id"), table_name="photos")
    op.drop_table("photos")
