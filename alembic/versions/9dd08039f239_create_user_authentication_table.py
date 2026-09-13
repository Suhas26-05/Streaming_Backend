"""create user authentication table

Revision ID: 9dd08039f239
Revises: 
Create Date: 2026-09-13 12:39:13.605923

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9dd08039f239'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
            "users",
            sa.Column("userId", sa.String(length=50), nullable=False),
            sa.Column("name", sa.String(length=50), nullable=False),
            sa.Column("email", sa.String(length=100), nullable=False),
            sa.Column("password", sa.String(length=255), nullable=False),
            sa.PrimaryKeyConstraint("userId"),
            sa.UniqueConstraint("email"),
        )
    
    op.create_index(
            op.f("ix_users_userId"),
            "users",
            ["userId"],
            unique=False
        )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_users_userId'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
