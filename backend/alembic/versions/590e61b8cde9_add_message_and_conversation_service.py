"""add message and conversation service

Revision ID: 590e61b8cde9
Revises: ee0a512d44d8
Create Date: 2026-08-04 16:00:32.684574

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision: str = '590e61b8cde9'
down_revision: Union[str, Sequence[str], None] = 'ee0a512d44d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
