from typing import Dict, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm.attributes import InstrumentedAttribute

from .helpers import has_session, has_pagination, has_sorting
from app.orm.base import PaginationSchema, SortingSchema, select
from app.orm.spell import SpellOrm
from app.models.spell import SpellModel
from app.orm.klass import KlassOrm
from app.orm.source import SourceOrm

router = APIRouter(
  prefix="/spells",
  tags=["spells"],
)

SORTABLES: Dict[str, InstrumentedAttribute] = {
  'id': SpellOrm.id,
  'name': SpellOrm.name,
  'charges': SpellOrm.charges,
  'class_id': SpellOrm.klass_id,
  'class_name': KlassOrm.name,
  'source_id': SpellOrm.source_id,
  'source_name': SourceOrm.name,
}

EAGER_LOAD_OPTIONS = [
  contains_eager(SpellOrm.klass),
  contains_eager(SpellOrm.source),
]

class IndexSchema(BaseModel):
  data: List[SpellModel]
  pagination: PaginationSchema

pagination_depend = has_pagination()
sorting_depend = has_sorting(SORTABLES, 'id')

@router.get("/", response_model=IndexSchema)
def index(session = Depends(has_session), pagination: PaginationSchema = Depends(pagination_depend), sorting: SortingSchema = Depends(sorting_depend)):
  spells_orm = select(SpellOrm).join(KlassOrm).join(SourceOrm).options(*EAGER_LOAD_OPTIONS).pagination(pagination).sorting(sorting).get_scalars(session)
  spells_model = SpellModel.from_orm_list(spells_orm)
  return IndexSchema(data=spells_model, pagination=pagination)

class GetSchema(BaseModel):
    data: SpellModel

@router.get("/{spell_id}", response_model=GetSchema)
def get(spell_id: str, session = Depends(has_session)):
  spell_orm = select(SpellOrm).where(SpellOrm.where_slug_or_id(spell_id)).join(KlassOrm).join(SourceOrm).options(*EAGER_LOAD_OPTIONS).get_scalar(session)
  spell_model =  SpellModel.from_orm(spell_orm)
  return GetSchema(data=spell_model)