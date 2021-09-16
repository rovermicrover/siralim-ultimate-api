from typing import Dict, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm.attributes import InstrumentedAttribute

from .helpers import has_session, has_pagination, has_sorting
from app.orm.base import PaginationSchema, SortingSchema, select
from app.orm.trait import TraitOrm
from app.models.trait import TraitModel

router = APIRouter(
  prefix="/traits",
  tags=["traits"],
)

SORTABLES: Dict[str, InstrumentedAttribute] = {
  'id': TraitOrm.id,
  'name': TraitOrm.name,
  'material_name': TraitOrm.material_name,
}

class IndexSchema(BaseModel):
  data: List[TraitModel]
  pagination: PaginationSchema

pagination_depend = has_pagination()
sorting_depend = has_sorting(SORTABLES, 'id')

@router.get("/", response_model=IndexSchema)
def index(session = Depends(has_session), pagination: PaginationSchema = Depends(pagination_depend), sorting: SortingSchema = Depends(sorting_depend)):
  traits_orm = select(TraitOrm).pagination(pagination).sorting(sorting).get_scalars(session)
  traits_model = TraitModel.from_orm_list(traits_orm)
  return IndexSchema(data=traits_model, pagination=pagination)

class GetSchema(BaseModel):
  data: TraitModel

@router.get("/{trait_id}", response_model=GetSchema)
def get(trait_id: str, session = Depends(has_session)):
  trait_orm = select(TraitOrm).where(TraitOrm.where_slug_or_id(trait_id)).get_scalar(session)
  trait_model = TraitModel.from_orm(trait_orm)
  return GetSchema(data=trait_model)