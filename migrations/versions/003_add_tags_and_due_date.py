"""Add tags and due_date for Cấp 6

Revision ID: 003
Revises: 002
Create Date: 2026-03-14 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add due_date column to todos
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('due_date', sa.Date(), nullable=True))
        batch_op.create_index(op.f('ix_todos_due_date'), ['due_date'], unique=False)
    
    # Create tags table
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_tags_name'), 'tags', ['name'], unique=True)
    
    # Create todo_tags association table
    op.create_table(
        'todo_tags',
        sa.Column('todo_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['todo_id'], ['todos.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('todo_id', 'tag_id')
    )


def downgrade() -> None:
    # Drop todo_tags table
    op.drop_table('todo_tags')
    
    # Drop tags table
    op.drop_index(op.f('ix_tags_name'), table_name='tags')
    op.drop_table('tags')
    
    # Remove due_date from todos
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.drop_index(op.f('ix_todos_due_date'))
        batch_op.drop_column('due_date')
