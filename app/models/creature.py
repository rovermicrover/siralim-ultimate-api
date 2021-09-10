from typing import List, Optional
from pydantic import BaseModel

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

    battle_sprite: str
    
    health: int
    attack: int
    intelligence: int
    defense: int
    speed: int
    
    klass: KlassModel
    race: RaceModel
    sources: List[SourceModel]
    trait: TraitModel

    class Config:
        orm_mode = True