"""Added unique for email

Revision ID: f08f3e23e587
Revises: dfa70687899c
Create Date: 2025-09-14 17:47:07.828403

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f08f3e23e587"
down_revision: Union[str, Sequence[str], None] = "dfa70687899c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
