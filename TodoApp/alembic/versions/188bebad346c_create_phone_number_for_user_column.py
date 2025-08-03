"""Create phone number for user column

Revision ID: 188bebad346c
Revises: 
Create Date: 2025-08-02 20:57:46.246463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '188bebad346c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema. use command alembic upgrade 188bebad346c  to apply this migration.""" 
    op.add_column(
        'users',
        sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema. used command 'alembic downgrade -1' to revert the last migration."""
    op.drop_column('users', 'phone_number')
    # Note: Downgrading will remove the phone_number column from the users table.
    # Ensure that this is acceptable for your application logic before applying this migration.
