"""init_core_schema

Revision ID: 043479096807
Revises: 
Create Date: 2026-06-30 21:37:02.857616

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '043479096807'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with open('db_migrations/01_init.sql', 'r') as f:
        sql = f.read()
    op.execute(sql)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS event_queue;")
    op.execute("DROP TABLE IF EXISTS costs;")
    op.execute("DROP TABLE IF EXISTS task_states;")
    op.execute("DROP TABLE IF EXISTS tasks;")
