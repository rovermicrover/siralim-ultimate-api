from __future__ import annotations
from datetime import datetime

from typing import List, Optional
from pydantic import BaseModel, Field

from .base import BaseModelOrm
from .klass import KlassModel
from .race import RaceModel
from .source import SourceModel
from .trait import TraitModel


class CreatureModel(BaseModel, BaseModelOrm):
    id: int
    name: str
    slug: str
    description: Optional[str] = None

    # url for battle sprite
    battle_sprite_url: str = Field(None, alias='battle_sprite')

    health: int
    attack: int
    intelligence: int
    defense: int
    speed: int

    klass: KlassModel
    race: RaceModel
    sources: List[SourceModel]
    trait: TraitModel

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        # The alias field must not ever be supplied else its contents will be used instead
        allow_population_by_field_name = True
