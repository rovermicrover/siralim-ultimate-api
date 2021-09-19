from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.dialects import postgresql

from .base import BaseOrm, build_slug_defaulter


class TraitOrm(BaseOrm):
    __tablename__ = "traits"

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

    material_name = Column(String(50))

    tags = Column(postgresql.ARRAY(Text))

    created_at = Column("created_at", TIMESTAMP, nullable=False)
    updated_at = Column("updated_at", TIMESTAMP, nullable=False)
