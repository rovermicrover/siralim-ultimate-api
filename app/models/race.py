from datetime import datetime

from typing import Optional
from pydantic import BaseModel

from .base import BaseModelOrm
from .klass import KlassModel


class RaceModel(BaseModel, BaseModelOrm):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    icon: str
    default_klass: KlassModel

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
