from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from .base import BaseOrm, build_slug_defaulter


class SpellOrm(BaseOrm):
    __tablename__ = "spells"

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

    charges = Column(Integer, nullable=False)

    klass_id = Column(Integer, ForeignKey("klasses.id"), nullable=False)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)

    klass = relationship(
        "KlassOrm", primaryjoin="SpellOrm.klass_id == KlassOrm.id"
    )
    source = relationship(
        "SourceOrm", primaryjoin="SpellOrm.source_id == SourceOrm.id"
    )

    klass_name = association_proxy("klass", "name")
    source_name = association_proxy("source", "name")

    tags = Column(postgresql.ARRAY(Text))
