"""add pgvector ivfflat index

Revision ID: a4518ae93431
Revises: 77c2a33e4e10
Create Date: 2026-08-03 11:28:40.300251

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision: str = 'a4518ae93431'
down_revision: Union[str, Sequence[str], None] = '77c2a33e4e10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass
    # op.execute("""
    #     CREATE INDEX IF NOT EXISTS
    #     idx_document_chunks_embedding

    #     ON document_chunks

    #     USING ivfflat
    #     (embedding vector_cosine_ops)

    #     WITH (lists = 20);
    # """)


def downgrade() -> None:
    """Downgrade schema."""
    pass
    # op.execute("""
    #     DROP INDEX IF EXISTS
    #     idx_document_chunks_embedding;
    # """)
