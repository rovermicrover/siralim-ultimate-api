from __future__ import annotations
from datetime import datetime

from typing import List, Optional
from pydantic import BaseModel, root_validator

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
    battle_sprite: str
    @root_validator(pre=False)
    def replace_sprite_with_url(cls, values):
        id_ = values['id']
        battle_sprite_url = f"/api/creatures/{id_}/images/battle_sprite.png"
        values['battle_sprite'] = battle_sprite_url
        return values

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
