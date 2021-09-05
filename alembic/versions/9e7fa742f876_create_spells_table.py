"""create spells table

Revision ID: 9e7fa742f876
Revises: 3b08542a8ab1
Create Date: 2021-08-30 23:07:13.353015

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e7fa742f876'
down_revision = '3b08542a8ab1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'spells',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('slug', sa.String(50), nullable=False, unique=True),
        sa.Column('description', sa.UnicodeText()),
        sa.Column('charges', sa.Integer, nullable=False),
        sa.Column('klass_id', sa.Integer, nullable=False),
        sa.Column('source_id', sa.Integer, nullable=False),
    )


def downgrade():
    op.drop_table('spells')
