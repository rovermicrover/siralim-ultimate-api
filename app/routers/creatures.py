from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import joinedload, selectinload

from .helpers import has_session, has_pagination
from app.orm.base import PaginationSchema
from app.orm.creature import CreatureOrm
from app.models.creature import CreatureModel
from app.orm.race import RaceOrm

router = APIRouter(
  prefix="/creatures",
  tags=["creatures"],
)

EAGER_LOAD_OPTIONS = [
  joinedload(CreatureOrm.klass),
  joinedload(CreatureOrm.race),
  joinedload(CreatureOrm.trait),
  joinedload(CreatureOrm.race, RaceOrm.default_klass),
  selectinload(CreatureOrm.sources),
]

class IndexSchema(BaseModel):
  data: List[CreatureModel]
  pagination: PaginationSchema

pagination_depend = has_pagination()

@router.get("/", response_model=IndexSchema)
def index(session = Depends(has_session), pagination: PaginationSchema = Depends(pagination_depend)):
  creatures_orm = CreatureOrm.get_all(session, eager_loads=EAGER_LOAD_OPTIONS, pagination=pagination)
  creatures_model = CreatureModel.from_orm_list(creatures_orm)
  return IndexSchema(data=creatures_model, pagination=pagination)

class GetSchema(BaseModel):
  data: CreatureModel

@router.get("/{creature_id}", response_model=GetSchema)
def get(creature_id: str, session = Depends(has_session)):
  creatures_orm = CreatureOrm.get_by_slug_or_id(session, creature_id, eager_loads=EAGER_LOAD_OPTIONS)
  creatures_model = CreatureModel.from_orm(creatures_orm)
  return GetSchema(data=creatures_model)
