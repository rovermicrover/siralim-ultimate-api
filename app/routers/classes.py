from typing import Dict, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm.attributes import InstrumentedAttribute

from .helpers import has_session, has_pagination, has_sorting
from app.orm.base import PaginationSchema, SortingSchema, select
from app.orm.klass import KlassOrm
from app.models.klass import KlassModel

router = APIRouter(
  prefix="/classes",
  tags=["classes"],
)

SORTABLES: Dict[str, InstrumentedAttribute] = {
  'id': KlassOrm.id,
  'name': KlassOrm.name,
}

class IndexSchema(BaseModel):
  data: List[KlassModel]
  pagination: PaginationSchema

pagination_depend = has_pagination(default_size=5)
sorting_depend = has_sorting(SORTABLES, 'id')

@router.get("/", response_model=IndexSchema)
def index(session = Depends(has_session), pagination: PaginationSchema = Depends(pagination_depend), sorting: SortingSchema = Depends(sorting_depend)):
  klasses_orm = select(KlassOrm).pagination(pagination).sorting(sorting).get_scalars(session)
  klasses_model = KlassModel.from_orm_list(klasses_orm)
  return IndexSchema(data=klasses_model, pagination=pagination)

class GetSchema(BaseModel):
  data: KlassModel

@router.get("/{klass_id}", response_model=GetSchema)
def get(klass_id: str, session = Depends(has_session)):
  klasses_orm = select(KlassOrm).where(KlassOrm.where_slug_or_id(klass_id)).get_scalar(session)
  klasses_model =  KlassModel.from_orm(klasses_orm)
  return GetSchema(data=klasses_model)
