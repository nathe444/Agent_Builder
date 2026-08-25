"""add chat and conversation model

Revision ID: 2c23ed144c2d
Revises: 47710d62f09d
Create Date: 2026-08-04 15:52:32.310170

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision: str = '2c23ed144c2d'
down_revision: Union[str, Sequence[str], None] = '47710d62f09d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
