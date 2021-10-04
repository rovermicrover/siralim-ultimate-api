"""perks table

Revision ID: 85bc789138fe
Revises: 14839378b87c
Create Date: 2021-10-02 00:19:38.266279

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '85bc789138fe'
down_revision = '14839378b87c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'perks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('slug', sa.String(50), nullable=False, unique=True),
        sa.Column('description', sa.Text()),
        sa.Column('icon', sa.Text()),
        sa.Column('ranks', sa.Integer, nullable=False),
        sa.Column('cost', sa.Integer, nullable=False),
        sa.Column('annointment', sa.Boolean, nullable=False),
        sa.Column('ascension', sa.Boolean, nullable=False),
        sa.Column('specialization_id', sa.Integer, nullable=False),
        sa.Column('tags', postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
    )


def downgrade():
    op.drop_table('perks')
