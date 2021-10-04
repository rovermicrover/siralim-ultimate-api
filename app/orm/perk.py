from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
    TIMESTAMP,
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from .base import BaseOrm, build_slug_defaulter, FullText


class PerkOrm(BaseOrm):
    __tablename__ = "perks"

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

    icon = Column(Text(), nullable=False)

    ranks = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)
    annointment = Column(Boolean, nullable=False)
    ascension = Column(Boolean, nullable=False)

    specialization_id = Column(
        Integer, ForeignKey("specializations.id"), nullable=False
    )

    specialization = relationship(
        "SpecializationOrm",
        primaryjoin="PerkOrm.specialization_id == SpecializationOrm.id",
    )

    specialization_name = association_proxy("specialization", "name")

    tags = Column(postgresql.ARRAY(Text))

    created_at = Column("created_at", TIMESTAMP, nullable=False)
    updated_at = Column("updated_at", TIMESTAMP, nullable=False)

    full_text = FullText(
        "full_text", "name", "description", "specialization_name"
    )
