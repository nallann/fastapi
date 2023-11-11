"""add content column to post table

Revision ID: 3f75cf6e3133
Revises: 98e1ddbbad0a
Create Date: 2023-11-06 17:22:13.098541

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f75cf6e3133'
down_revision: Union[str, None] = '98e1ddbbad0a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column("content", sa.String(), nullable=False))



def downgrade() -> None:
    op.drop_column("posts", "content")

