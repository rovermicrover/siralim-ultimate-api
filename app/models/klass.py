from datetime import datetime

from typing import Optional
from pydantic import BaseModel
from pydantic.fields import Field

from .base import BaseModelOrm


class KlassModel(BaseModel, BaseModelOrm):
    id: int
    name: str
    slug: str
    description: Optional[str] = None

    color: str
    icon_url: str = Field(None, alias='icon')

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        # The alias field must never be supplied else its contents will be used instead
        allow_population_by_field_name = True
