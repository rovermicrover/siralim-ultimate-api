from app.orm.trait import TraitOrm
from app.orm.klass import KlassOrm
from typing import Dict, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import contains_eager, selectinload
from sqlalchemy.orm.attributes import InstrumentedAttribute

from .helpers import PaginationSchema, SortingSchema, select, has_session, has_pagination, has_sorting
from app.orm.creature import CreatureOrm
from app.models.creature import CreatureModel
from app.orm.race import RaceOrm

router = APIRouter(
  prefix="/creatures",
  tags=["creatures"],
)

SORTABLES: Dict[str, InstrumentedAttribute] = {
  'id': CreatureOrm.id,
  'name': CreatureOrm.name,
  'health': CreatureOrm.health,
  'attack': CreatureOrm.attack,
  'intelligence': CreatureOrm.intelligence,
  'defense': CreatureOrm.defense,
  'speed': CreatureOrm.speed,
  'class_id': CreatureOrm.klass_id,
  'class_name': KlassOrm.name,
  'race_id': CreatureOrm.race_id,
  'race_name': RaceOrm.name,
  'trait_id': CreatureOrm.trait_id,
  'trait_name': TraitOrm.name,
}

EAGER_LOAD_OPTIONS = (
  contains_eager(CreatureOrm.klass),
  contains_eager(CreatureOrm.race),
  contains_eager(CreatureOrm.trait),
  selectinload(CreatureOrm.race, RaceOrm.default_klass),
  selectinload(CreatureOrm.sources),
)

class IndexSchema(BaseModel):
  data: List[CreatureModel]
  pagination: PaginationSchema

pagination_depend = has_pagination()
sorting_depend = has_sorting(SORTABLES, 'id')

@router.get("/", response_model=IndexSchema)
def index(session = Depends(has_session), pagination: PaginationSchema = Depends(pagination_depend), sorting: SortingSchema = Depends(sorting_depend)):
  creatures_orm = select(CreatureOrm).join(RaceOrm).join(KlassOrm, CreatureOrm.klass_id == KlassOrm.id).join(TraitOrm).options(*EAGER_LOAD_OPTIONS).pagination(pagination).sorting(sorting).get_scalars(session)
  creatures_model = CreatureModel.from_orm_list(creatures_orm)
  return IndexSchema(data=creatures_model, pagination=pagination)

class GetSchema(BaseModel):
  data: CreatureModel

@router.get("/{creature_id}", response_model=GetSchema)
def get(creature_id: str, session = Depends(has_session)):
  creatures_orm = select(CreatureOrm).where(CreatureOrm.where_slug_or_id(creature_id)).join(RaceOrm).join(KlassOrm, CreatureOrm.klass_id == KlassOrm.id).join(TraitOrm).options(*EAGER_LOAD_OPTIONS).get_scalar(session)
  creatures_model = CreatureModel.from_orm(creatures_orm)
  return GetSchema(data=creatures_model)
