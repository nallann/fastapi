"""add last few columns to post table

Revision ID: 1c7ff6d136fd
Revises: 8edbcb522a62
Create Date: 2023-11-06 17:55:13.688016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c7ff6d136fd'
down_revision: Union[str, None] = '8edbcb522a62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", 
                  sa.Column("published", sa.Boolean(), nullable=False, server_default="True"))
    op.add_column("posts",
                  sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")))


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
