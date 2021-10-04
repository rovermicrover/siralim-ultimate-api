"""specializations table

Revision ID: 14839378b87c
Revises: c768498b4cf2
Create Date: 2021-10-02 00:19:31.940328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14839378b87c'
down_revision = 'c768498b4cf2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'specializations',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('slug', sa.String(50), nullable=False, unique=True),
        sa.Column('description', sa.Text()),
        sa.Column('icon', sa.Text()),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
    )


def downgrade():
    op.drop_table('specializations')
