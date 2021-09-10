from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .helpers import has_session, has_pagination
from app.orm.base import PaginationSchema
from app.orm.klass import KlassOrm
from app.models.klass import KlassModel

router = APIRouter(
  prefix="/classes",
  tags=["classes"],
)

class IndexSchema(BaseModel):
  data: List[KlassModel]
  pagination: PaginationSchema

pagination_depend = has_pagination(default_size=5)

@router.get("/", response_model=IndexSchema)
def index(session = Depends(has_session), pagination: PaginationSchema = Depends(pagination_depend)):
  klasses_orm = KlassOrm.get_all(session)
  klasses_model = KlassModel.from_orm_list(klasses_orm, pagination=pagination)
  return IndexSchema(data=klasses_model, pagination=pagination)

class GetSchema(BaseModel):
  data: KlassModel

@router.get("/{klass_id}", response_model=GetSchema)
def get(klass_id: str, session = Depends(has_session)):
  klasses_orm = KlassOrm.get_by_slug_or_id(session, klass_id)
  klasses_model =  KlassModel.from_orm(klasses_orm)
  return GetSchema(data=klasses_model)
