from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import relationship

from .base import BaseOrm, build_slug_defaulter


class SourceOrm(BaseOrm):
    __tablename__ = "sources"

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

    creatures = relationship("CreatureOrm", back_populates="sources")
    spells = relationship("SpellOrm", back_populates="source")

    created_at = Column("created_at", TIMESTAMP, nullable=False)
    updated_at = Column("updated_at", TIMESTAMP, nullable=False)
