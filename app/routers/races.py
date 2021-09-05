from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import joinedload

from app.orm.base import has_session
from app.orm.race import RaceOrm
from app.models.race import RaceModel

router = APIRouter(
  prefix="/races",
  tags=["races"],
)

EAGER_LOAD_OPTIONS = [
  joinedload(RaceOrm.default_klass)
]

class IndexSchema(BaseModel):
  data: List[RaceModel]

@router.get("/", response_model=IndexSchema)
def index(session = Depends(has_session)):
  races_orm = RaceOrm.get_all(session, options=EAGER_LOAD_OPTIONS)
  races_model = RaceModel.from_orm_list(races_orm)
  return IndexSchema(data=races_model)

class GetSchema(BaseModel):
  data: RaceModel

@router.get("/{race_id}", response_model=GetSchema)
def get(race_id: str, session = Depends(has_session)):
  races_orm = RaceOrm.get_by_slug_or_id(session, race_id, options=EAGER_LOAD_OPTIONS)
  races_model = RaceModel.from_orm(races_orm)
  return GetSchema(data=races_model)