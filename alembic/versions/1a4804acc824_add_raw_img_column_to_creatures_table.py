"""add raw img column to creatures table

Revision ID: 1a4804acc824
Revises: 85bc789138fe
Create Date: 2021-10-11 04:24:03.926897

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import table, column
from sqlalchemy import String
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.sqltypes import Integer, LargeBinary

from app.orm.creature import convert_from_base64_img_tag_data

# revision identifiers, used by Alembic.
revision = '1a4804acc824'
down_revision = '85bc789138fe'
branch_labels = None
depends_on = None
import logging
LOG = logging.getLogger(__file__)

RAW_COLUMN = 'battle_sprite_raw'
B64_COLUMN = 'battle_sprite'

def upgrade():
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('creatures', sa.Column(RAW_COLUMN, sa.LargeBinary(), nullable=True))
	# ### end Alembic commands ###
    # decode base64 image back into png
    creature = table('creatures',column('id', Integer), column(B64_COLUMN, String), column(RAW_COLUMN, LargeBinary))
    
    results = session.execute(select(creature.c.id, creature.c.battle_sprite))
    for (id_, data) in results:
        png = convert_from_base64_img_tag_data(data)
        session.execute(creature
        .update()
        .where(creature.c.id == id_)
        .values(battle_sprite_raw=png,)
        )
    
    op.alter_column('creatures', RAW_COLUMN, nullable=False)



def downgrade():
    op.drop_column('creatures', RAW_COLUMN)
    # ### end Alembic commands ###