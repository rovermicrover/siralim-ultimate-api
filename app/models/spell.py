from typing import List, Optional
from pydantic import BaseModel

from .base import BaseModelOrm
from .klass import KlassModel
from .source import SourceModel


class SpellModel(BaseModel, BaseModelOrm):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    charges: int
    klass: KlassModel
    source: SourceModel

    tags: List[str]

    class Config:
        orm_mode = True
