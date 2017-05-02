"""create test table

Revision ID: c9f476989c56
Revises: 
Create Date: 2017-03-11 21:45:01.499411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9f476989c56'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('login', sa.String(150), nullable=False),
        sa.Column('password', sa.String(150), nullable=False),
        sa.Column('user_role', sa.String(150), server_default='admin'),
        #sa.Column('search_queries_id', sa.Integer, sa.ForeignKey('queries.id', name='fk_queries_id')),
        #sa.Column('search_queries_id', sa.Integer, nullable=True),
        #sa.ForeignKeyConstraint(['search_queries_id'], ['queries.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'queries',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('search_query', sa.String(150)),
        sa.Column('date', sa.DateTime),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', name='fk_user_id')),
        #sa.Column('user_id', sa.Integer, nullable=True),
        #sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    pass
