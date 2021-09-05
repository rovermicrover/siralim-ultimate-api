"""create races table

Revision ID: 229bb5a494dc
Revises: 43aeae93213e
Create Date: 2021-08-30 23:13:01.574461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '229bb5a494dc'
down_revision = '43aeae93213e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'races',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('slug', sa.String(50), nullable=False, unique=True),
        sa.Column('description', sa.UnicodeText()),
        sa.Column('default_klass_id', sa.Integer, nullable=False),
    )


def downgrade():
    op.drop_table('races')
