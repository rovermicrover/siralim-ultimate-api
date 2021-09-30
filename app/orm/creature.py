from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from .base import BaseOrm, build_slug_defaulter, FullText


class CreatureOrm(BaseOrm):
    __tablename__ = "creatures"

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

    battle_sprite = Column(Text(), nullable=False)

    health = Column("health", Integer, nullable=False)
    attack = Column("attack", Integer, nullable=False)
    intelligence = Column("intelligence", Integer, nullable=False)
    defense = Column("defense", Integer, nullable=False)
    speed = Column("speed", Integer, nullable=False)

    klass_id = Column(Integer, ForeignKey("klasses.id"), nullable=False)
    race_id = Column(Integer, ForeignKey("races.id"), nullable=False)
    trait_id = Column(Integer, ForeignKey("traits.id"), nullable=False)
    source_ids = Column(Integer, ForeignKey("sources.id"), nullable=False)

    klass = relationship("KlassOrm")
    race = relationship("RaceOrm")
    trait = relationship("TraitOrm")
    sources = relationship(
        "SourceOrm",
        primaryjoin="SourceOrm.id == any_(foreign(CreatureOrm.source_ids))",
        uselist=True,
    )

    klass_name = association_proxy("klass", "name")
    race_name = association_proxy("race", "name")
    trait_name = association_proxy("trait", "name")
    trait_description = association_proxy("trait", "description")
    trait_tags = association_proxy("trait", "tags")

    created_at = Column("created_at", TIMESTAMP, nullable=False)
    updated_at = Column("updated_at", TIMESTAMP, nullable=False)

    full_text = FullText(
        "full_text", "name", "description", "trait_name", "trait_description", "race_name", "klass_name"
    )
