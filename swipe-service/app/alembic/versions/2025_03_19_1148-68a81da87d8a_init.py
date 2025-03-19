"""init

Revision ID: 68a81da87d8a
Revises:
Create Date: 2025-03-19 11:48:31.265147

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "68a81da87d8a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "swipes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("profile_id_1", sa.Integer(), nullable=False),
        sa.Column("profile_id_2", sa.Integer(), nullable=False),
        sa.Column("decision_1", sa.Boolean(), nullable=True),
        sa.Column("decision_2", sa.Boolean(), nullable=True),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_swipes")),
    )
    op.create_index(
        op.f("ix_swipes_profile_id_1"), "swipes", ["profile_id_1"], unique=False
    )
    op.create_index(
        op.f("ix_swipes_profile_id_2"), "swipes", ["profile_id_2"], unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_swipes_profile_id_2"), table_name="swipes")
    op.drop_index(op.f("ix_swipes_profile_id_1"), table_name="swipes")
    op.drop_table("swipes")
