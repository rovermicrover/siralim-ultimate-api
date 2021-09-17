from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseOrm, build_slug_defaulter


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

    default_klass_id = Column(
        Integer, ForeignKey("klasses.id"), nullable=False
    )

    default_klass = relationship(
        "KlassOrm", primaryjoin="RaceOrm.default_klass_id == KlassOrm.id"
    )
