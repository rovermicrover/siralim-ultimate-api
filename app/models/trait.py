from datetime import datetime

from typing import List, Optional
from pydantic import BaseModel

from .base import BaseModelOrm


class TraitModel(BaseModel, BaseModelOrm):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    material_name: Optional[str] = None

    tags: List[str]

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
