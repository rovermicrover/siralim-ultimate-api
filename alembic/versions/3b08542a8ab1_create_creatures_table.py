"""create creatures table

Revision ID: 3b08542a8ab1
Revises: 6cf9cef6fc82
Create Date: 2021-08-30 23:07:10.067012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b08542a8ab1'
down_revision = '6cf9cef6fc82'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'creatures',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('slug', sa.String(50), nullable=False, unique=True),
        sa.Column('description', sa.Text()),
        sa.Column('battle_sprite', sa.Text(), nullable=False),
        sa.Column('klass_id', sa.Integer, nullable=False),
        sa.Column('race_id', sa.Integer, nullable=False),
        sa.Column('trait_id', sa.Integer, nullable=False),
        sa.Column('health', sa.Integer, nullable=False),
        sa.Column('attack', sa.Integer, nullable=False),
        sa.Column('intelligence', sa.Integer, nullable=False),
        sa.Column('defense', sa.Integer, nullable=False),
        sa.Column('speed', sa.Integer, nullable=False),
        sa.Column('source_ids', sa.ARRAY(sa.Integer), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
    )


def downgrade():
    op.drop_table('creatures')
