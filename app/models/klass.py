from typing import Optional
from pydantic import BaseModel

from .base import BaseModelOrm


class KlassModel(BaseModel, BaseModelOrm):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    color: str

    class Config:
        orm_mode = True
