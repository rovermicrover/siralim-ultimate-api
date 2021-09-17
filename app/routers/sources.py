from typing import Dict, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm.attributes import InstrumentedAttribute

from .helpers import (
    PaginationSchema,
    SortingSchema,
    select,
    has_session,
    has_pagination,
    has_sorting,
)
from app.orm.source import SourceOrm
from app.models.source import SourceModel

router = APIRouter(
    prefix="/sources",
    tags=["sources"],
)

SORTABLES: Dict[str, InstrumentedAttribute] = {
    "id": SourceOrm.id,
    "name": SourceOrm.name,
}


class IndexSchema(BaseModel):
    data: List[SourceModel]
    pagination: PaginationSchema


pagination_depend = has_pagination()
sorting_depend = has_sorting(SORTABLES, "id")


@router.get("/", response_model=IndexSchema)
def index(
    session=Depends(has_session),
    pagination: PaginationSchema = Depends(pagination_depend),
    sorting: SortingSchema = Depends(sorting_depend),
):
    sources_orm = (
        select(SourceOrm)
        .pagination(pagination)
        .sorting(sorting)
        .get_scalars(session)
    )
    sources_model = SourceModel.from_orm_list(sources_orm)
    return IndexSchema(data=sources_model, pagination=pagination)


class GetSchema(BaseModel):
    data: SourceModel


@router.get("/{source_id}", response_model=GetSchema)
def get(source_id: str, session=Depends(has_session)):
    source_orm = (
        select(SourceOrm)
        .where(SourceOrm.where_slug_or_id(source_id))
        .get_scalar(session)
    )
    source_model = SourceModel.from_orm(source_orm)
    return GetSchema(data=source_model)
