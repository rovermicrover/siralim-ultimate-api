from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql.sqltypes import LargeBinary
from sqlalchemy.util.langhelpers import hybridproperty

from app.orm.creature import convert_from_base64_img_tag_data
from .base import BaseOrm, build_slug_defaulter, FullText

def default_img_data(context) -> bytes:
    b64 = context.get_current_parameters()['icon']
    return convert_from_base64_img_tag_data(b64)


class KlassOrm(BaseOrm):
    __tablename__ = "klasses"

    slug_defaulter = build_slug_defaulter("name")

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    slug = Column(
        String(50),
        nullable=False,
        unique=True,
        default=slug_defaulter,
        onupdate=slug_defaulter,
    )
    description = Column(Text())

    color = Column(String(10), nullable=False)
    icon_b64 = Column('icon', Text(), nullable=False)
    icon_raw = Column('icon_raw', LargeBinary, nullable=False, default=default_img_data)

    @hybridproperty
    def icon_url(self):
        val =  f"/api/classes/{self.id}/images/icon.png"
        return val

    created_at = Column("created_at", TIMESTAMP, nullable=False)
    updated_at = Column("updated_at", TIMESTAMP, nullable=False)
