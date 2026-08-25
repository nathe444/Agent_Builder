"""add chat and conversation model

Revision ID: ee0a512d44d8
Revises: 2c23ed144c2d
Create Date: 2026-08-04 15:54:04.034444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision: str = 'ee0a512d44d8'
down_revision: Union[str, Sequence[str], None] = '2c23ed144c2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
