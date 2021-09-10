"""create sources table

Revision ID: 02d84d31d7a7
Revises: 229bb5a494dc
Create Date: 2021-08-30 23:19:28.442574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02d84d31d7a7'
down_revision = '229bb5a494dc'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'sources',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('slug', sa.String(50), nullable=False, unique=True),
        sa.Column('description', sa.Text()),
    )


def downgrade():
    op.drop_table('sources')
