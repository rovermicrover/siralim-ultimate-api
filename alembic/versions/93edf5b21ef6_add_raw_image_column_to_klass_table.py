"""add raw image column to klass table

Revision ID: 93edf5b21ef6
Revises: 1a4804acc824
Create Date: 2021-10-11 21:47:09.420963

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.expression import column, select, table
from sqlalchemy.sql.sqltypes import Integer, LargeBinary, String
from sqlalchemy.sql.type_api import INTEGERTYPE

from app.orm.creature import convert_from_base64_img_tag_data

# revision identifiers, used by Alembic.
revision = '93edf5b21ef6'
down_revision = '1a4804acc824'
branch_labels = None
depends_on = None

RAW_COLUMN = 'icon_raw'
B64_COLUMN = 'icon'

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('klasses', sa.Column('icon_raw', sa.LargeBinary(), nullable=True))
    # ### end Alembic commands ###
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)


    klass = table('klasses',column('id', Integer), column(B64_COLUMN, String), column(RAW_COLUMN, LargeBinary))
    
    results = session.execute(select(klass.c.id, klass.c.icon))
    for (id_, data) in results:
        png = convert_from_base64_img_tag_data(data)
        session.execute(klass
        .update()
        .where(klass.c.id == id_)
        .values(icon_raw=png,)
        )
    
    op.alter_column('klasses', RAW_COLUMN, nullable=False)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('klasses', 'icon_raw')
    # ### end Alembic commands ###
