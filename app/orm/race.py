from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql.sqltypes import LargeBinary

from .base import BaseOrm, build_slug_defaulter, FullText
from app.orm.creature import convert_from_base64_img_tag_data

def default_img_data(context) -> bytes:
    b64 = context.get_current_parameters()['icon']
    return convert_from_base64_img_tag_data(b64)


class RaceOrm(BaseOrm):
    __tablename__ = "races"

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

    icon = Column('icon', Text(), nullable=False)
    icon_raw = Column('icon_raw', LargeBinary, nullable=False, default=default_img_data)

    default_klass_id = Column(
        Integer, ForeignKey("klasses.id"), nullable=False
    )

    default_klass = relationship(
        "KlassOrm", primaryjoin="RaceOrm.default_klass_id == KlassOrm.id"
    )

    default_klass_name = association_proxy("default_klass", "name")

    created_at = Column("created_at", TIMESTAMP, nullable=False)
    updated_at = Column("updated_at", TIMESTAMP, nullable=False)

    full_text = FullText("full_text", "name", "description")
