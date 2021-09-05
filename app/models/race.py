from typing import Optional
from pydantic import BaseModel

from .base import BaseModelOrm
from .klass import KlassModel

class RaceModel(BaseModel, BaseModelOrm):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    default_klass: KlassModel

    class Config:
        orm_mode = True