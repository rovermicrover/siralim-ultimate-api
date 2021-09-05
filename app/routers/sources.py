from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.orm.base import has_session
from app.orm.source import SourceOrm
from app.models.source import SourceModel

router = APIRouter(
  prefix="/sources",
  tags=["sources"],
)

class IndexSchema(BaseModel):
    data: List[SourceModel]

@router.get("/", response_model=IndexSchema)
def index(session = Depends(has_session)):
  sources_orm = SourceOrm.get_all(session)
  sources_model = SourceModel.from_orm_list(sources_orm)
  return IndexSchema(data=sources_model)

class GetSchema(BaseModel):
    data: SourceModel

@router.get("/{source_id}", response_model=GetSchema)
def get(source_id: str, session = Depends(has_session)):
  source_orm = SourceOrm.get_by_slug_or_id(session, source_id)
  source_model = SourceModel.from_orm(source_orm)
  return GetSchema(data=source_model)