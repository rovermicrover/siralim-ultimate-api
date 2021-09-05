from sqlalchemy import Column, Integer, String, Unicode, ForeignKey
from .base import BaseOrm, build_slug_defaulter

class TraitOrm(BaseOrm):
  __tablename__ = "traits"

  slug_defaulter = build_slug_defaulter("name")

  id = Column(Integer, primary_key=True)
  name = Column(String(50), nullable=False)
  slug = Column(String(50), nullable=False, unique=True, default=slug_defaulter, onupdate=slug_defaulter)
  material_name = Column(String(50))
  description = Column(Unicode(200))