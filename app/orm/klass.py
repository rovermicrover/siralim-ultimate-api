from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql.sqltypes import LargeBinary

from .base import BaseOrm, build_slug_defaulter, FullText


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
    icon = Column('icon', Text(), nullable=False)
    icon_raw = Column('icon_raw', LargeBinary, nullable=False)

    created_at = Column("created_at", TIMESTAMP, nullable=False)
    updated_at = Column("updated_at", TIMESTAMP, nullable=False)
