from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import joinedload

from .helpers import has_session, has_pagination
from app.orm.base import PaginationSchema
from app.orm.spell import SpellOrm
from app.models.spell import SpellModel

router = APIRouter(
  prefix="/spells",
  tags=["spells"],
)

EAGER_LOAD_OPTIONS = [
  joinedload(SpellOrm.klass),
  joinedload(SpellOrm.source),
]

class IndexSchema(BaseModel):
  data: List[SpellModel]
  pagination: PaginationSchema

pagination_depend = has_pagination()

@router.get("/", response_model=IndexSchema)
def index(session = Depends(has_session), pagination: PaginationSchema = Depends(pagination_depend)):
  spells_orm = SpellOrm.get_all(session, eager_loads=EAGER_LOAD_OPTIONS)
  spells_model = SpellModel.from_orm_list(spells_orm)
  return IndexSchema(data=spells_model, pagination=pagination)

class GetSchema(BaseModel):
    data: SpellModel

@router.get("/{spell_id}", response_model=GetSchema)
def get(spell_id: str, session = Depends(has_session)):
  spell_orm = SpellOrm.get_by_slug_or_id(session, spell_id, eager_loads=EAGER_LOAD_OPTIONS)
  spell_model =  SpellModel.from_orm(spell_orm)
  return GetSchema(data=spell_model)