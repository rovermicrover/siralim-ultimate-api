"""create classes table

Revision ID: 43aeae93213e
Revises:
Create Date: 2021-08-30 23:13:07.107773

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43aeae93213e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'klasses',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('slug', sa.String(50), nullable=False, unique=True),
        sa.Column('description', sa.Text()),
        sa.Column('color', sa.String(10), nullable=False),
        sa.Column('icon', sa.Text(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
    )


def downgrade():
    op.drop_table('klasses')
