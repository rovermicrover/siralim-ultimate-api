"""create status effects table

Revision ID: 1d5aa0ce2503
Revises: 9e7fa742f876
Create Date: 2021-09-14 22:30:28.650101

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '1d5aa0ce2503'
down_revision = '9e7fa742f876'
branch_labels = None
depends_on = None


def upgrade():
    postgresql
    op.create_table(
        'status_effects',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('slug', sa.String(50), nullable=False, unique=True),
        sa.Column('description', sa.Text()),
        sa.Column("category", sa.Enum("buff", "debuff", "minion", name="status_effects_categories", create_type=False)),
        sa.Column('icon', sa.Text(), nullable=False),
        sa.Column('turns', sa.Integer),
        sa.Column('leave_chance', sa.Integer),
        sa.Column('max_stacks', sa.Integer, nullable=False),
    )


def downgrade():
    op.drop_table('status_effects')
