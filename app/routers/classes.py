from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.orm.base import has_session
from app.orm.klass import KlassOrm
from app.models.klass import KlassModel

router = APIRouter(
  prefix="/classes",
  tags=["classes"],
)

class IndexSchema(BaseModel):
  data: List[KlassModel]

@router.get("/", response_model=IndexSchema)
def index(session = Depends(has_session)):
  klasses_orm = KlassOrm.get_all(session)
  klasses_model = KlassModel.from_orm_list(klasses_orm)
  return IndexSchema(data=klasses_model)

class GetSchema(BaseModel):
  data: KlassModel

@router.get("/{klass_id}", response_model=GetSchema)
def get(klass_id: str, session = Depends(has_session)):
  klasses_orm = KlassOrm.get_by_slug_or_id(session, klass_id)
  klasses_model =  KlassModel.from_orm(klasses_orm)
  return GetSchema(data=klasses_model)
