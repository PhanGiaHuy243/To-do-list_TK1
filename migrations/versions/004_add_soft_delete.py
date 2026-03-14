"""Add soft delete (deleted_at) for Cấp 8

Revision ID: 004
Revises: 003
Create Date: 2026-03-14 13:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add deleted_at column to todos
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted_at', sa.DateTime(), nullable=True))
        batch_op.create_index(op.f('ix_todos_deleted_at'), ['deleted_at'], unique=False)


def downgrade() -> None:
    # Remove deleted_at column from todos
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.drop_index(op.f('ix_todos_deleted_at'))
        batch_op.drop_column('deleted_at')
