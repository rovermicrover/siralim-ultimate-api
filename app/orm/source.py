from sqlalchemy import Column, Integer, String, Unicode, ForeignKey, event
from sqlalchemy.orm import relationship
from .base import BaseOrm, build_slug_defaulter

class SourceOrm(BaseOrm):
  __tablename__ = "sources"

  slug_defaulter = build_slug_defaulter("name")

  id = Column(Integer, primary_key=True)
  name = Column(String(50), nullable=False)
  slug = Column(String(50), nullable=False, unique=True, default=slug_defaulter, onupdate=slug_defaulter)
  description = Column(Unicode(200))

  creatures = relationship("CreatureOrm", back_populates="sources")
  spells = relationship("SpellOrm", back_populates="source")