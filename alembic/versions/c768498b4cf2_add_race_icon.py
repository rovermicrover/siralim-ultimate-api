"""Add race icon

Revision ID: c768498b4cf2
Revises: 1d5aa0ce2503
Create Date: 2021-09-29 22:58:52.197188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c768498b4cf2'
down_revision = '1d5aa0ce2503'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('races', sa.Column('icon', sa.Text()))


def downgrade():
    op.drop_column('races', 'icon')
