"""fixed a typo in rooms facilities table

Revision ID: 6687fb118b77
Revises: 1b06e9cfcb75
Create Date: 2025-10-26 22:29:43.517511

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6687fb118b77"
down_revision: Union[str, Sequence[str], None] = "1b06e9cfcb75"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "rooms_facilities", sa.Column("room_id", sa.Integer(), nullable=False)
    )
    op.drop_constraint(
        op.f("rooms_facilities_rooms_id_fkey"), "rooms_facilities", type_="foreignkey"
    )
    op.create_foreign_key(None, "rooms_facilities", "rooms", ["room_id"], ["id"])
    op.drop_column("rooms_facilities", "rooms_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "rooms_facilities",
        sa.Column("rooms_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "rooms_facilities", type_="foreignkey")
    op.create_foreign_key(
        op.f("rooms_facilities_rooms_id_fkey"),
        "rooms_facilities",
        "rooms",
        ["rooms_id"],
        ["id"],
    )
    op.drop_column("rooms_facilities", "room_id")
