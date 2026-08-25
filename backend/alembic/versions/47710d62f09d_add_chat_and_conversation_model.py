"""add chat and conversation model

Revision ID: 47710d62f09d
Revises: a4518ae93431
Create Date: 2026-08-04 15:50:44.552814

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision: str = '47710d62f09d'
down_revision: Union[str, Sequence[str], None] = 'a4518ae93431'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
