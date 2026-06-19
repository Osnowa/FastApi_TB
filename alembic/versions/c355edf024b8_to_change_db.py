"""to change DB

Revision ID: c355edf024b8
Revises: 59325f9d0b9a
Create Date: 2026-06-19 23:13:48.959899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c355edf024b8'
down_revision: Union[str, Sequence[str], None] = '59325f9d0b9a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table('tasks') as batch_op:
        # Вместо op.alter_column используем batch_op.alter_column
        batch_op.alter_column(
            'priority',
            existing_type=sa.INTEGER(), # Важно: укажите существующий тип
            type_=sa.Enum('low', 'medium', 'high', name='priority'),
            existing_nullable=True
        )

def downgrade():
    with op.batch_alter_table('tasks') as batch_op:
        batch_op.alter_column(
            'priority',
            existing_type=sa.Enum('low', 'medium', 'high', name='priority'),
            type_=sa.INTEGER(),
            existing_nullable=True
        )
