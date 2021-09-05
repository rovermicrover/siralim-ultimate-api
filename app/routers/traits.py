from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.orm.base import has_session
from app.orm.trait import TraitOrm
from app.models.trait import TraitModel

router = APIRouter(
  prefix="/traits",
  tags=["traits"],
)

class IndexSchema(BaseModel):
    data: List[TraitModel]

@router.get("/", response_model=IndexSchema)
def index(session = Depends(has_session)):
  trais_orm = TraitOrm.get_all(session)
  traits_model = TraitModel.from_orm_list(trais_orm)
  return IndexSchema(data=traits_model)

class GetSchema(BaseModel):
    data: TraitModel

@router.get("/{trait_id}", response_model=GetSchema)
def get(trait_id: str, session = Depends(has_session)):
  trait_orm = TraitOrm.get_by_slug_or_id(session, trait_id)
  trait_model = TraitModel.from_orm(trait_orm)
  return GetSchema(data=trait_model)