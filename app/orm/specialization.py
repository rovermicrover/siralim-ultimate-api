from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import relationship

from .base import BaseOrm, build_slug_defaulter, FullText


class SpecializationOrm(BaseOrm):
    __tablename__ = "specializations"

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

    icon = Column(Text())

    perks = relationship("PerkOrm", back_populates="specialization")

    created_at = Column("created_at", TIMESTAMP, nullable=False)
    updated_at = Column("updated_at", TIMESTAMP, nullable=False)

    full_text = FullText("full_text", "name", "description")
