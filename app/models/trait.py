from typing import Optional
from pydantic import BaseModel

from .base import BaseModelOrm

class TraitModel(BaseModel, BaseModelOrm):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    material_name: Optional[str] = None

    class Config:
        orm_mode = True