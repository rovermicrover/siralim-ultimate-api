from datetime import datetime

from typing import List, Optional
from pydantic import BaseModel

from .base import BaseModelOrm
from .specialization import SpecializationModel


class PerkModel(BaseModel, BaseModelOrm):
    id: int
    name: str
    slug: str
    description: Optional[str] = None

    icon: Optional[str] = None
    ranks: int
    cost: int
    annointment: bool
    ascension: bool
    specialization: SpecializationModel

    tags: List[str]

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
