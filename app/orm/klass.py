from sqlalchemy import Column, Integer, String, Text
from .base import BaseOrm, build_slug_defaulter

class KlassOrm(BaseOrm):
  __tablename__ = "klasses"

  slug_defaulter = build_slug_defaulter("name")

  id = Column(Integer, primary_key=True)
  name = Column(String(50), nullable=False)
  slug = Column(String(50), nullable=False, unique=True, default=slug_defaulter, onupdate=slug_defaulter)
  description = Column(Text())
  
  color = Column(String(10), nullable=False)