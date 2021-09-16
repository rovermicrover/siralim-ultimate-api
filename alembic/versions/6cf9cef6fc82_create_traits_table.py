"""create traits table

Revision ID: 6cf9cef6fc82
Revises: 02d84d31d7a7
Create Date: 2021-08-30 23:07:17.203732

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '6cf9cef6fc82'
down_revision = '02d84d31d7a7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'traits',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('slug', sa.String(50), nullable=False, unique=True),
        sa.Column('material_name', sa.String(50)),
        sa.Column('description', sa.Text()),
        sa.Column('tags', postgresql.ARRAY(sa.Text()), nullable=False),
    )


def downgrade():
    op.drop_table('traits')
