from datetime import datetime

from typing import Optional
from pydantic import BaseModel

from .base import BaseModelOrm
from app.common.status_effect import StatusEffectCategoriesEnum


class StatusEffectModel(BaseModel, BaseModelOrm):
    id: int
    name: str
    slug: str
    description: Optional[str] = None

    category: StatusEffectCategoriesEnum

    icon: str

    turns: Optional[int] = None
    leave_chance: Optional[int] = None
    max_stacks: int

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
