"""Add users table and owner_id to todos

Revision ID: 002
Revises: 001
Create Date: 2026-03-14 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_is_active'), 'users', ['is_active'], unique=False)
    
    # Add owner_id to todos (SQLite batch mode)
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('owner_id', sa.Integer(), nullable=False, server_default='1'))
        batch_op.create_foreign_key('fk_todos_owner_id', 'users', ['owner_id'], ['id'])
        batch_op.create_index(op.f('ix_todos_owner_id'), ['owner_id'], unique=False)


def downgrade() -> None:
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.drop_index(op.f('ix_todos_owner_id'))
        batch_op.drop_constraint('fk_todos_owner_id', type_='foreignkey')
        batch_op.drop_column('owner_id')
    
    op.drop_index(op.f('ix_users_is_active'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
